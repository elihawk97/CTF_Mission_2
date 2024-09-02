import subprocess
import threading
from cryptography.fernet import Fernet
import socket
import json
import traceback
import os
import time
import file_decrypter
import sys
import tempfile

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


HOST = '127.0.0.1'  # Localhost
PORT = 10923        # Port to listen on
CORRECT_EMAIL = 'darwish@hamas.aza'  # The correct email address
PCAP_FILE_PATH = 'ignore/hamas_communications.pcapng.ignore'  # Path to your PCAP file
CHUNK_SIZE = 4096  # Size of chunks to send

def send_file(client_socket, file_path):
    file = file_decrypter.decrypt_file(file_path)[1]
    file_size = len(file)
    client_socket.send(json.dumps({'status': 'success', 'file_size': file_size, 'Message': 'Top Secret \n Do Not Share. \n Sending secure packet capture in 5 seconds...'}).encode('utf-8'))
    time.sleep(5)
    file = decrypt_file(file_path)[1]
    offset = 0
    while offset < len(file):
        chunk = file[offset:offset + CHUNK_SIZE]
        client_socket.sendall(chunk)
        offset += CHUNK_SIZE
        # Indicate end of transmission
    print("File sent successfully.")
def handle_client(client_socket):
    try:
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                message = json.loads(data)
                if 'email' in message:
                    if (message['email']).lower() == CORRECT_EMAIL:
                        send_file(client_socket, PCAP_FILE_PATH)
                        return  # Exit after sending file
                    else:
                        response = {'status': 'failure', 'message': 'Incorrect email address'}
                else:
                    response = {'status': 'error', 'message': 'Invalid message format', 'hint':'We have received reports that: adJust textS On operatioNs.'}

                client_socket.send(json.dumps(response).encode('utf-8'))

            except json.JSONDecodeError:
                response = {'status': 'error', 'message': 'Invalid JSON format'}
                client_socket.send(json.dumps(response).encode('utf-8'))
            except Exception as e:
                response = {'status': 'error', 'message': f'Server error: {str(e)}'}
                client_socket.send(json.dumps(response).encode('utf-8'))

    except Exception as e:
        print(f"Error handling client: {str(e)}")
    finally:
        client_socket.close()

def start_server():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Server listening...")

            while True:
                try:
                    conn, addr = s.accept()
                    print(f"Connected by {addr}")
                    handle_client(conn)
                except Exception as e:
                    print(f"Error accepting connection: {str(e)}")
    except Exception as e:
        print(f"Server error: {str(e)}")
        print(traceback.format_exc())

# Function to play a video
def play_video(video_path):
    try:
        subprocess.run(['start', video_path], shell=True)
    except Exception as e:
        print(f"Failed to play video: {e}")

# Function to run the server script
def run_server_script(script_path):
    try:
        subprocess.run(['python', script_path], shell=True)
    except Exception as e:
        print(f"Failed to run server script: {e}")



if __name__ == "__main__":
    # Path to the video file and server script
    video_file = "ignore/final_video.mp4"  # Replace with your actual video file

    # Start the server in a background thread
    server_thread = threading.Thread(target=start_server, args=())
    server_thread.start()
    # Play the video
    play_video(video_file)

    # Wait for the server thread to finish (optional)
    server_thread.join()
