import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# Function to encrypt a message
def encrypt_message(message, key):
    # Convert message to bytes
    message_bytes = message.encode('utf-8')

    # Pad the message to make its length a multiple of the block size (16 bytes for AES)
    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(message_bytes) + padder.finalize()

    # Generate a random 16-byte initialization vector (IV)
    iv = os.urandom(16)

    # Create the AES cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the padded message
    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()

    # Encode the IV and the encrypted message in Base64
    encrypted_message_base64 = base64.urlsafe_b64encode(iv + encrypted_message).decode('utf-8')

    return encrypted_message_base64

# Function to decrypt a message
def decrypt_message(encrypted_message_base64, key):
    # Decode the Base64-encoded encrypted message
    encrypted_message_bytes = base64.urlsafe_b64decode(encrypted_message_base64.encode('utf-8'))

    # Extract the IV and the encrypted message
    iv = encrypted_message_bytes[:16]
    encrypted_message = encrypted_message_bytes[16:]

    # Create the AES cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the message
    decrypted_padded_message = decryptor.update(encrypted_message) + decryptor.finalize()

    # Unpad the decrypted message
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()

    return decrypted_message.decode('utf-8')

# Example usage
if __name__ == "__main__":
    # 32-byte key for AES-256 (must be 16, 24, or 32 bytes long)
    key = "StrongerTogether".encode('ascii')#os.urandom(32)
    #print(key.encode())
    original_message = "Lattitude Coordinate: 1) 33.7125983731065"

    # Encrypt the message
    encrypted_message = encrypt_message(original_message, key)
    print(f"Encrypted message (Base64): {encrypted_message}")

    # Decrypt the message
    decrypted_message = decrypt_message(encrypted_message, key)
    print(f"Decrypted message: {decrypted_message}")
