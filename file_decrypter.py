from cryptography.fernet import Fernet
import subprocess

# The key used for encryption
key = b'lQpxAKZNp4BBvBdIr6kCAGz3RjXtFTpLOpLPD5NlO_s='
def decrypt_file(encrypted_file):
    cipher = Fernet(key)
   # files = ["final_video.mp4.ignore", "tcp_server.py.ignore", "hamas_communications.pcapng.ignore"]
    decrypted_file = ""
    # Decrypt the file
    with open(encrypted_file, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = cipher.decrypt(encrypted_data)
    # Remove the '.ignore' extension and store the data in the dictionary
    original_filename = encrypted_file.replace(".ignore", "")
    return (original_filename, decrypted_data)

# Now you can use 'secret_data_decrypted.txt' within your script
