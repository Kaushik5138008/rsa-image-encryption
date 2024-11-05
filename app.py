from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
import uuid
from rsa_utils import RSA_image_encryption  # Import RSA encryption function

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# In-memory storage for active channel keys
active_channels = {}

def generate_channel_key():
    return str(uuid.uuid4().int)[:6]  # Generate a 6-digit unique key

def clear_previous_images():
    """Delete all files in the encrypted and decrypted directories."""
    encrypted_dir = os.path.join('static', 'encrypted_images')
    decrypted_dir = os.path.join('static', 'decrypted_images')
    
    # Clear encrypted images
    if os.path.exists(encrypted_dir):
        for filename in os.listdir(encrypted_dir):
            file_path = os.path.join(encrypted_dir, filename)
            os.remove(file_path)
    
    # Clear decrypted images
    if os.path.exists(decrypted_dir):
        for filename in os.listdir(decrypted_dir):
            file_path = os.path.join(decrypted_dir, filename)
            os.remove(file_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_channel', methods=['GET', 'POST'])
def create_channel():
    if request.method == 'POST':
        # Clear previous images when creating a new channel
        clear_previous_images()
        
        # Generate a new channel key
        channel_key = generate_channel_key()
        
        # Store the generated channel key in active channels
        active_channels[channel_key] = {'users': []}
        
        # Store the channel key in the session
        session['channel_key'] = channel_key
        
        # Clear previous session paths for images
        session.pop('encrypted_image_paths', None)
        session.pop('decrypted_image_paths', None)
        
        return redirect(url_for('choose_role', channel_key=channel_key))
    
    return render_template('create_channel.html')

@app.route('/join_channel', methods=['GET', 'POST'])
def join_channel():
    if request.method == 'POST':
        channel_key = request.form['channel_key']
        
        # Check if the channel key exists in active channels
        if channel_key in active_channels:
            session['channel_key'] = channel_key
            return redirect(url_for('choose_role', channel_key=channel_key))
        else:
            flash("Invalid channel key. Please try again.")
            return redirect(url_for('join_channel'))
    
    return render_template('join_channel.html')

@app.route('/choose_role/<channel_key>', methods=['GET', 'POST'])
def choose_role(channel_key):
    # Validate that the channel_key is still active
    if channel_key not in active_channels:
        flash("Invalid channel key. Please start or join a valid channel.")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        role = request.form['role']
        session['role'] = role
        
        # Add user to the channel's user list
        if 'channel_key' in session:
            active_channels[session['channel_key']]['users'].append(role)
        
        return redirect(url_for(role, channel_key=channel_key))
    
    return render_template('choose_role.html', channel_key=channel_key)

@app.route('/sender/<channel_key>', methods=['GET', 'POST'])
def sender(channel_key):
    if channel_key not in active_channels:
        return redirect(url_for('index'))

    if request.method == 'POST':
        images = request.files.getlist('image')  # Get multiple files
        encrypted_paths = []
        decrypted_paths = []

        if images:
            encrypted_dir = os.path.join('static', 'encrypted_images')
            decrypted_dir = os.path.join('static', 'decrypted_images')
            os.makedirs(encrypted_dir, exist_ok=True)
            os.makedirs(decrypted_dir, exist_ok=True)

            for image in images:
                image_path = os.path.join('static', 'uploads', image.filename)
                image.save(image_path)

                # Encrypt the image using RSA
                encrypted_output_path, decrypted_output_path = RSA_image_encryption(image_path)

                # Move encrypted and decrypted images to respective folders
                encrypted_filename = os.path.join(encrypted_dir, os.path.basename(encrypted_output_path))
                decrypted_filename = os.path.join(decrypted_dir, os.path.basename(decrypted_output_path))
                os.rename(encrypted_output_path, encrypted_filename)
                os.rename(decrypted_output_path, decrypted_filename)

                encrypted_paths.append(f"encrypted_images/{os.path.basename(encrypted_filename)}")
                decrypted_paths.append(f"decrypted_images/{os.path.basename(decrypted_filename)}")

            # Save paths in session
            session['encrypted_image_paths'] = encrypted_paths
            session['decrypted_image_paths'] = decrypted_paths

            # Notify interceptor and receiver
            socketio.emit('new_image', {'encrypted_paths': encrypted_paths}, room=channel_key)
            flash('Images uploaded and encrypted successfully!')
    
    return render_template('sender.html', channel_key=channel_key)

@socketio.on('join')
def on_join(data):
    channel_key = data['channel_key']
    join_room(channel_key)
    emit('user_joined', {'message': f"A new user has joined channel {channel_key}."}, room=channel_key)

@app.route('/interceptor/<channel_key>')
def interceptor(channel_key):
    if channel_key not in active_channels:
        return redirect(url_for('index'))
    
    encrypted_image_paths = session.get('encrypted_image_paths', [])
    return render_template('interceptor.html', channel_key=channel_key, encrypted_image_paths=encrypted_image_paths)

@app.route('/receiver/<channel_key>')
def receiver(channel_key):
    if channel_key not in active_channels:
        return redirect(url_for('index'))
    
    decrypted_image_paths = session.get('decrypted_image_paths', [])
    return render_template('receiver.html', channel_key=channel_key, decrypted_image_paths=decrypted_image_paths)

if __name__ == '__main__':
    os.makedirs('static/uploads', exist_ok=True)
    socketio.run(app, debug=True)
