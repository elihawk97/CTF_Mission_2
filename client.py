import socket
import json
import sys
import os

# Configuration
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 10923        # The port used by the server
CHUNK_SIZE = 4096   # Size of chunks to receive
OUTPUT_FILE = 'received_challenge.pcap'  # Name of the file to save

def receive_file(sock, file_size):
    received_size = 0
    with open(OUTPUT_FILE, 'wb') as file:
        while received_size < file_size:
            chunk = sock.recv(min(CHUNK_SIZE, file_size - received_size))
            if not chunk:
                raise Exception("Connection closed before receiving complete file")
            file.write(chunk)
            received_size += len(chunk)
    print(f"File received and saved as {OUTPUT_FILE}")

def send_message(email):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #s.settimeout(30)  # Set a timeout of 5 seconds
            s.connect((HOST, PORT))
            message = json.dumps({'email': email})
            s.sendall(message.encode('utf-8'))

            response = s.recv(1024).decode('utf-8')
            response_data = json.loads(response)

            if response_data['status'] == 'success':
                file_size = response_data['file_size']
                print(response_data['Message'])
                print(f"Correct email! Receiving PCAP file ({file_size} bytes)...")
                receive_file(s, file_size)
                return True
            else:
                print(f"Server response: {response_data['message']}")
                return False

    except socket.timeout:
        print("Connection timed out. The server might be down or unreachable.")
    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running and the address is correct.")
    except json.JSONDecodeError:
        print("Received invalid JSON from server.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    return False

def main():
    while True:
        try:
            email = input("Enter the email address (or 'quit' to exit): ")
            if email.lower() == 'quit':
                break

            if send_message(email):
                break  # Exit if file was received successfully

        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
