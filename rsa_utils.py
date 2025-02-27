from PIL import Image
import numpy as np
import cv2 as cv
import os
def RSA_image_encryption(image_path):
    # RSA Encryption Function
    p = 61
    q = 53
    def RSA_encrypt(value, e, n):
        return pow(value, e, n)

    # RSA Decryption Function
    def RSA_decrypt(value, d, n):
        return pow(value, d, n)

    # Function to convert color image to integer array
    def image_to_int_array(image_path):
        img = cv.imread(image_path)  # Read the image in color mode (BGR)
        if img is None:
            raise ValueError(f"Image not found at path: {image_path}")
        
        # Split the image into B, G, R channels
        b, g, r = cv.split(img)
        
        # Flatten each channel and combine into a single array
        data = np.concatenate([b.flatten(), g.flatten(), r.flatten()])
        
        return data, img.shape

    # Function to convert integer array back to color image
    def int_array_to_image(int_array, size, output_path):
        # Calculate the size of each channel
        int_array = [x % 256 for x in int_array]
        channel_size = size[0] * size[1]
        
        # Split the flat array into three separate channels
        b = np.array(int_array[:channel_size], dtype=np.uint8).reshape(size[:2])
        g = np.array(int_array[channel_size:2*channel_size], dtype=np.uint8).reshape(size[:2])
        r = np.array(int_array[2*channel_size:], dtype=np.uint8).reshape(size[:2])
        
        # Merge the channels back into a BGR image
        img = cv.merge((b, g, r))
        
        # Convert the array to a PIL image and save
        img_pil = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))
        img_pil.save(output_path)

    # RSA Encryption for an image
    # Convert image to integer array
    int_array, size = image_to_int_array(image_path)
    
    # RSA Key Generation
    n = p * q
    o = (p - 1) * (q - 1)
    
    # Choose e, public key
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a
    
    e = 3
    while gcd(e, o) != 1:
        e += 2
    
    # Calculate the private key d
    def modular_inverse(e, o):
        def egcd(a, b):
            x0, x1, y0, y1 = 1, 0, 0, 1
            while b:
                q, a, b = a // b, b, a % b
                x0, x1 = x1, x0 - q * x1
                y0, y1 = y1, y0 - q * y1
            return a, x0, y0

        g, x, _ = egcd(e, o)
        if g != 1:
            raise Exception('Modular inverse does not exist')
        else:
            return x % o

    d = modular_inverse(e, o)

    # Encrypt each pixel value
    encrypted_array = [RSA_encrypt(int(pixel), e, n) for pixel in int_array]
    
    # Save encrypted data as an image
    encrypted_output_path = f"encrypted_images/encrypted_{os.path.basename(image_path)}"
    int_array_to_image(encrypted_array, size, encrypted_output_path)

    # Decrypt the encrypted array
    decrypted_array = [RSA_decrypt(pixel, d, n) for pixel in encrypted_array]
    
    # Convert decrypted values back to the range [0, 255]
    decrypted_array = [min(max(value, 0), 255) for value in decrypted_array]
    
    # Save decrypted image
    decrypted_output_path = f"decrypted_images/decrypted_{os.path.basename(image_path)}"
    int_array_to_image(decrypted_array, size, decrypted_output_path)

    return encrypted_output_path, decrypted_output_path