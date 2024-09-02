def xor_encrypt_decrypt(message, key):
    encrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(message, key * len(message)))
    return encrypted

# Final Coordinate: 33.71259837310654, 73.03283493301709

# Example usage
key = "HamasWar"  # Keep it simple and repeatable
message = "Lattitude Coordinate: 1) 33.71259837310654"
encrypted_message = xor_encrypt_decrypt(message, key)

print("Key:", key)
print("Encrypted Message:", encrypted_message)
