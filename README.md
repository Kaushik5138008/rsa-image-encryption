# RSA Image Encryption System  

## Project Overview  
This project is a **Flask-based web application** that enables users to securely share images using **RSA encryption**. It supports real-time communication using **Flask-SocketIO**, allowing multiple users to participate in an encrypted image transfer system.

---

## Features  
✅ **Channel-based communication** – Users can create and join unique channels.  
✅ **Image encryption with RSA** – Securely encrypt and decrypt images.  
✅ **Multi-user support** – Roles include sender, interceptor, and receiver.  
✅ **Flask-SocketIO integration** – Real-time notifications when images are uploaded.  
✅ **Automatic image cleanup** – Removes old images upon new session creation.  

---

## Project Structure  
```
project/
│── static/
│   ├── encrypted_images/      # Stores encrypted images
│   ├── decrypted_images/      # Stores decrypted images
│   ├── uploads/               # Stores uploaded images before encryption
│── templates/                 # HTML templates for Flask frontend
│── app.py                     # Main Flask application
│── rsa_utils.py               # RSA encryption functions
│── bulk.ipynb                 # Jupyter Notebook for batch encryption
│── __pycache__/                # Python cache files (ignore)
│── README.md                   # Project documentation
│── requirements.txt            # Python dependencies
```

---

## Setup Instructions  

### **1. Clone the Repository**
```sh
git clone https://github.com/Kaushik5138008/rsa-image-encryption.git
cd rsa-image-encryption
```

### **2. Install Dependencies**  
Ensure **Python 3.8+** is installed. Then, run:
```sh
pip install -r requirements.txt
```

### **3. Run the Flask Application**  
```sh
python app.py
```
or with Flask’s development server:
```sh
flask run
```

### **4. Access the Web App**  
Open your browser and go to:  
👉 **http://127.0.0.1:5000/**  

---

## Usage  
### **Roles in the System**
- **Sender** – Uploads images and encrypts them before sending.  
- **Interceptor** – Views the encrypted images.  
- **Receiver** – Decrypts images and retrieves the original version.  

### **How It Works**
1. **Create a Channel** – Generates a unique key for secure communication.  
2. **Join a Channel** – Other users enter the key to access the same session.  
3. **Upload an Image** – The sender selects images to encrypt using RSA.  
4. **Intercept Encrypted Image** – The interceptor can view the encrypted version.  
5. **Receive & Decrypt** – The receiver gets the decrypted image.  

---

## Flask Routes  
| Route | Method | Description |
|--------|--------|-------------|
| `/` | `GET` | Homepage |
| `/create_channel` | `POST` | Creates a new encrypted channel |
| `/join_channel` | `POST` | Joins an existing channel |
| `/choose_role/<channel_key>` | `POST` | Selects sender, interceptor, or receiver |
| `/sender/<channel_key>` | `POST` | Uploads and encrypts images |
| `/interceptor/<channel_key>` | `GET` | Displays encrypted images |
| `/receiver/<channel_key>` | `GET` | Displays decrypted images |

---

## WebSocket Events  
| Event | Trigger | Action |
|--------|---------|---------|
| `join` | User joins a channel | Adds the user to the WebSocket room |
| `new_image` | Sender uploads an image | Notifies all users in the channel |
| `user_joined` | A user joins a session | Sends a message to all channel members |

---

## Dependencies  
📌 **Flask** – Web framework  
📌 **Flask-SocketIO** – Real-time WebSocket communication  
📌 **Pillow** – Image processing  
📌 **PyCryptodome** – RSA encryption library  

To install:
```sh
pip install Flask Flask-SocketIO Pillow pycryptodome
```

---

## Security Considerations  
🔒 **Session-based storage** – Active users are managed using Flask sessions.  
🔒 **RSA encryption** – Images are secured with asymmetric encryption.  
🔒 **Automatic cleanup** – Old images are removed to maintain security.  

---

## Contributing  
1. **Fork the repository**  
2. **Create a new branch** (`feature-branch`)  
3. **Commit changes**  
4. **Push to GitHub**  
5. **Submit a pull request**  

---

## License  
This project is for educational purposes. Feel free to use and modify it.


📌 Developed by **Team Flames** 
