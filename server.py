import socket
import json
import traceback
import os
import time
import file_decrypter

# Configuration
HOST = '127.0.0.1'  # Localhost
PORT = 10923        # Port to listen on
CORRECT_EMAIL = 'ctf_challenge@example.com'  # The correct email address
PCAP_FILE_PATH = 'hamas_communications.pcapng.ignore'  # Path to your PCAP file
CHUNK_SIZE = 4096  # Size of chunks to send

def send_file(client_socket, file_path):
    file = file_decrypter.decrypt_file(file_path)[1]
    file_size = len(file)
    client_socket.send(json.dumps({'status': 'success', 'file_size': file_size, 'Message': 'Top Secret \n Do Not Share. \n Sending secure packet capture in 5 seconds...'}).encode('utf-8'))
    time.sleep(5)
    file = file_decrypter.decrypt_file(file_path)[1]
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
                    if message['email'] == CORRECT_EMAIL:
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
            print(f"Server listening on {HOST}:{PORT}")

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

if __name__ == "__main__":
    start_server()
