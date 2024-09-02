import socket

def receive_audio_file(filename, host='localhost', port=5000):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Receive the audio data
    with open(filename, 'wb') as f:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            f.write(data)

    print(f"Audio file received and saved as {filename}.")

    client_socket.close()

# Replace 'received_audio.wav' with the desired file name for the received audio
receive_audio_file('received_audio.wav')
