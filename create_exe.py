import subprocess
import threading
from cryptography.fernet import Fernet
import json
import file_decrypter
from tkinter import PhotoImage
import pygame
from scapy.all import *
import time
import random
from dnslib import DNSRecord, QTYPE, RR, A, DNSHeader
import socket
import socketserver
import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button

def show_custom_message(title, message, bg_color, text_color, font, width=300, height=150):
    # Create a new top-level window
    msg_window = Toplevel()
    msg_window.title(title)

    # Set the size and background color
    msg_window.geometry(f"{width}x{height}")
    msg_window.configure(bg=bg_color)

    # Create and place the message label
    label = Label(msg_window, text=message, bg=bg_color, fg=text_color, font=font)
    label.pack(expand=True)

    # Create and place the OK button to close the window
    button = Button(msg_window, text="OK", command=msg_window.destroy)
    button.pack()

    # Center the window on the screen
    msg_window.update_idletasks()
    x = (msg_window.winfo_screenwidth() - width) // 2
    y = (msg_window.winfo_screenheight() - height) // 2
    msg_window.geometry(f"+{x}+{y}")


# Get the local IP address
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# DNS server configuration
DOMAIN_TO_IP = {
    'a.com.': local_ip,
    'b.com.': local_ip,
    # DNS table with 5 entries
    "olivetrees.com." : "73.032.34.33",
    "example.com.": "93.184.216.34",
    "google.com.": "172.217.16.142",
    "github.com.": "140.82.121.4",
    "stackoverflow.com.": "151.101.1.69",
    "python.org.": "138.197.63.241",
}

class DNSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        try:
            request = DNSRecord.parse(data)
           # print(f"Received request for: {str(request.q.qname)}")

            # Create a DNS response with the same ID and the appropriate flags
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

            qname = str(request.q.qname)
            qtype = QTYPE[request.q.qtype]

            if qname in DOMAIN_TO_IP:
                if qname == "olivetrees.com.":
                    reply.add_answer(RR(qname + "73.03283493301709", QTYPE.A, rdata=A(DOMAIN_TO_IP[qname])))
                else:
                    reply.add_answer(RR(qname, QTYPE.A, rdata=A(DOMAIN_TO_IP[qname])))
                #print(f"Resolved {qname} to {DOMAIN_TO_IP[qname]}")
            #else:
               # print(f"No record found for {qname}")

            socket.sendto(reply.pack(), self.client_address)
        except Exception as e:
            print(f"Error handling request: {e}")


def start_dns():
    server = socketserver.UDPServer(("0.0.0.0", 53533), DNSHandler)
    #print("DNS Server is running...")
    server.serve_forever()


def dns_query(domain, server_ip, source_port):
    try:
        dns_req = IP(dst='127.0.0.1', src="127.0.0.1")/UDP(dport=53533, sport=source_port)/DNS(rd=1, qd=DNSQR(qname=domain))
        answer = sr1(dns_req, verbose=0, timeout=2)
        if answer and answer.haslayer(DNS):
            if answer[DNS].ancount > 0:
                return answer[DNS].an.rdata
            else:
                return "No answer section in the response"
        elif answer:
            return f"Received non-DNS response: {answer.summary()}"
        else:
            return "No response received"
    except Exception as e:
        return f"An error occurred: {e}"

def start_dns_clients():
    server_ip = '127.0.0.1'
    #print(f"Using DNS server IP: {server_ip}")

    domains = ["example.com", "google.com", "github.com", "stackoverflow.com", "python.org", "nonexistent.com", "olivetrees.com"]
    for i in range(10):
        try:
            source_port = random.randint(20000, 30000)
            for domain in domains:
                result = dns_query(domain, server_ip, source_port)
                #print(f"{domain}: {result}")
        except:
            continue # do nothing
        time.sleep(15)


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
        flag = True
        while flag:
            try:
                client_socket.settimeout(10.0)  # 10 seconds timeout
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                if '101' in data:
                    flag = False
                else:
                    message = json.loads(data)
                if 'email' in message:
                    if (message['email']).lower() == CORRECT_EMAIL:
                        send_file(client_socket, PCAP_FILE_PATH)
                        return  # Exit after sending file
                    else:
                        response = {'status': 'failure', 'message': 'Incorrect email address'}
                else:
                    response = {'status': 'error', 'message': 'Invalid message format, include email', 'hint':'We have received reports that: adJust textS On operatioNs.'}

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
        return flag

def start_server():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Server listening...")
            flag = True
            while flag:
                try:
                    conn, addr = s.accept()
                    print(f"Connected by {addr}, once all data is received send code 101 to shutdown server"
                          f"this will restrict access to intruders.")
                    flag = handle_client(conn)
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

def show_hint_window(stage):
    hints = {
        1: "Proceed with caution. You have reached a point of no return.",
        2: "Update: Symmetric encryption expected. Also Watch out for An audio Voice recording.",
        3: "It is believed that Darwish has started a covert operation to fund a new Hamas operation through"
           "planting olive groves near Jewish towns in the Yehuda V'Shomron. They have gained access to DNS"
           "servers all over the world.",
        4: "We have just received intelligence that our international agency systems have been compromised."
           "Locate his city of refugee and get out immediately, time is of the essence."
    }

    # Create the pop-up window
    root = tk.Tk()
    root.withdraw()

    if stage in hints:
        hint_window = tk.Toplevel(root)
        hint_window.title("Mission Briefing")

        # Add a themed background image
        hint_window.geometry("400x300")
        background_image = PhotoImage(file="ignore/star_of_david_image.png")  # Use your own image
        background_label = tk.Label(hint_window, image=background_image)
        background_label.place(relwidth=1, relheight=1)

        if stage != 1:
        # Add a spy-themed header
            header = tk.Label(hint_window, text=f"{stage}", font=("Courier", 18, "bold"), fg="#00FF00", bg="black")
        else:
            header = tk.Label(hint_window, text=f"CTF", font=("Courier", 18, "bold"), fg="#00FF00", bg="black")
        header.pack(pady=10)

        # Display the hint text
        hint_text = tk.Label(hint_window, text=hints[stage], font=("Courier", 12), fg="#FFFF00", bg="black", wraplength=350)
        hint_text.pack(pady=20)

        # Add a "Proceed" button
        proceed_button = tk.Button(hint_window, text="Proceed", command=hint_window.destroy, font=("Courier", 12, "bold"), fg="white", bg="#FF0000")
        proceed_button.pack(pady=20)

        root.wait_window(hint_window)

    # if stage == 4:
    #     final_flag = simpledialog.askstring("Final Flag", "Enter the final flag:")
    #     if final_flag == "correct_final_flag":  # Replace with the actual final flag
    #         play_video("ignore/final_video.mp4")
    #         messagebox.showinfo("Mission Accomplished", "Congratulations! You've completed the mission!")

    root.destroy()

# Music Player
def music_player():
        # Initialize pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("ignore/amber.mp3")

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Function to start the password check window
def final_location():
    # Correct password
    correct_password = "islamabad"

    # Create the main window
    root = tk.Tk()
    root.title("Airstrike Location")
    root.geometry("300x150")
    root.configure(bg="black")

    # Spy-themed label
    label = tk.Label(root, text="Enter City:", font=("Courier", 14), fg="lime", bg="black")
    label.pack(pady=10)

    # Entry field for password
    entry = tk.Entry(root, font=("Courier", 14), fg="lime", bg="black")
    entry.pack(pady=10)

    # Function to check password
    def check_password():
        user_input = entry.get()
        if user_input == correct_password:
            #root.destroy()  # Close the pop-up
            root = tk.Tk()
            root.withdraw()
            # Custom message box for "Roger that, airstrike inbound"
            show_custom_message(
                title="Operation Command",
                message="Roger that, airstrike inbound",
                bg_color="blue",
                text_color="white",
                font=("Arial", 14, "bold"),
                width=350,
                height=200
            )


            # Custom message box for "Mission Accomplished"
            show_custom_message(
                title="Mission Status",
                message="Mission Accomplished",
                bg_color="green",
                text_color="white",
                font=("Arial", 16, "bold"),
                width=350,
                height=200
            )
            # Load the image and convert it for Tkinter
           # img = ImageTk.PhotoImage(Image.open("ignore/hussan_killed.jpg"))

            # Display the image using a Label
           # Label(root, image=img).pack()
            root.mainloop()
            # Uncomment to play video after password is correct
            # play_video('final_video.mp4')
        else:
            messagebox.showerror("Access Denied", "Incorrect password, intruder detected!")

    # Submit button
    button = tk.Button(root, text="Enter", font=("Courier", 14), command=check_password, fg="lime", bg="black")
    button.pack(pady=10)

    # Start the GUI loop
    root.mainloop()





# Function to start the password check window
def start_password_check_window():
    # Correct password
    correct_password = "33.71259837310654"

    # Create the main window
    root = tk.Tk()
    root.title("Spy Access Panel")
    root.geometry("300x150")
    root.configure(bg="black")

    # Spy-themed label
    label = tk.Label(root, text="Enter Coordinate:", font=("Courier", 14), fg="lime", bg="black")
    label.pack(pady=10)

    # Entry field for password
    entry = tk.Entry(root, font=("Courier", 14), show="*", fg="lime", bg="black")
    entry.pack(pady=10)

    # Function to check password
    def check_password():
        user_input = entry.get()
        if user_input == correct_password:
            #root.after(8000, root.destroy)
            root.destroy()  # Close the pop-up
            messagebox._show("Access Granted", "Welcome, Mr. Darwish")

            # Uncomment to play video after password is correct
            # play_video('final_video.mp4')
        else:
            messagebox.showerror("Access Denied", "Incorrect password, intruder detected!")

    # Submit button
    button = tk.Button(root, text="Enter", font=("Courier", 14), command=check_password, fg="lime", bg="black")
    button.pack(pady=10)

    # Start the GUI loop
    root.mainloop()





if __name__ == "__main__":
    # Path to the video file and server script
    video_file = "ignore/final_video.mp4"  # Replace with your actual video file


     # Play the video
    play_video(video_file)
    time.sleep(2)
    # Start the server in a background thread
    server_thread = threading.Thread(target=start_server, args=())
    server_thread.start()
    threading.Thread(target=show_hint_window(1)).start()
    server_thread.join()

    # Stage 2:
    show_hint_window(2)
    thread2 = threading.Thread(target=start_password_check_window)
    thread2.start()
    thread2.join()


    # Stage 3 with DNS
    show_hint_window(3)
    # Activate the DNS servers
    threading.Thread(target=start_dns).start()
    threading.Thread(target=start_dns_clients).start()
    music_player()
    show_hint_window(4)
    threading.Thread(target=final_location).start()


    # Wait for the server thread to finish (optional)
    #server2_thread.join()
