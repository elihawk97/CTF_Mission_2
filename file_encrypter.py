from cryptography.fernet import Fernet

# Generate a key and save it (this should be stored securely within your exe)
key = b'lQpxAKZNp4BBvBdIr6kCAGz3RjXtFTpLOpLPD5NlO_s='
cipher = Fernet(key)

files = ["server.py"]
# Encrypt the file
for file in files:
    with open(file, "rb") as current:
        encrypted_data = cipher.encrypt(current.read())

    with open(file + ".ignore", "wb") as current:
        current.write(encrypted_data)

print(f"Key: {key.decode()}")  # You need to use this key in your exe
