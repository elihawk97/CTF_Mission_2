import socket

def send_audio_file(filename, host='localhost', port=5000):
    # Read the audio file
    with open(filename, 'rb') as f:
        audio_data = f.read()

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}...")
    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        # Send the audio data
        conn.sendall(audio_data)
        print("Audio file sent.")
        conn.close()
   # server_socket.close()

# Replace 'your_audio_file.wav' with the path to your actual audio file
send_audio_file('combined_audio_secret.wav')
