import re
def xor_encrypt_decrypt(message, key):
    encrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(message, key * len(message)))
    return encrypted

def remove_single_spaces(text):
    # Replace all occurrences of single spaces with an empty string
    text = re.sub(r'(?<! ) (?! )', '', text)

    # Replace occurrences of multiple spaces with a single space
    text = re.sub(r' {2,}', ' ', text)

    return text

key = "HamasWar"  # Keep it simple and repeatable
encrypted_message = " #-A.%& IwP[hR^ODfSGqY^V@fQD}U"
#encrypted_message = remove_single_spaces(encrypted_message)
print(encrypted_message)
# Decrypting          #-A.%& IwP[hR^ODfSGqY^V@fQD}U
decrypted_message = xor_encrypt_decrypt(encrypted_message, key)
print("Decrypted Message:", decrypted_message)
