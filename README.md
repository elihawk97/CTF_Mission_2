# CTF_Mission
Infiltrate enemy servers, intercept communications, and locate the Hamas leader, Muhammad Ismail Darwish. This repo provides tools and a mission briefing video to immerse you in a high-stakes operation. National security is at risk—move fast, Agent.
## Storyline
### Operation: Silent Pursuit

Welcome, Agent. You've been tasked with a covert mission that will test your every skill. Deep within the heart of enemy territory, the notorious figurehead of Hamas, Muhammad Ismail Darwish, is plotting his next move. Your mission is to infiltrate the enemy's secure servers, intercept crucial communications, and pinpoint Darwish's location before he can disappear into the shadows once again.

This repository contains the tools you'll need to execute this high-stakes operation. The mission briefing video sets the stage with chilling clarity, as cryptic messages and flickering images reveal the depth of the threat. In the background, ominous music underscores the gravity of your task. The code here integrates audiovisual elements that immerse you into the heart of this mission, making every second count as you race against time.

Are you ready to face the unknown and bring a dangerous adversary to justice? The future of national security depends on you. Move fast, Agent. The clock is ticking.

## prerequisites
### Python Environment
* Python 3.10 is recommended, although 3.8 and on should work smoothly
* Python Packeges: Scapy, socket, sys, os
* Wireshark
* The executables should run smooth without any requirment beyond having the other files in the folder in the spot they came in, but these tools are needed to solve the CTF
### Skills Required
* Encryption
* Working with packet captures in wireshark
* DNS protocol
* HTTP protocol
* Socket Programming
* SQL (Injection ;)
* Working with audio files (can you figure out which type :)
* TCP/UDP/IP
* Scapy
###
* The "ignore" folder is not for your curious eyes, the files and information needed to solve the CTF will be given to you throughout the game as you need it.
* All information needed to solve the CTF is given to you either with the files and programs given to you or with hints at the beginning of the various stages. (Look around and you will find.)
* At certain points there will be a pop up box asking for a "secret code" (or something of that sort), input the information you found, if it doesn't work check spelling or maybe you're missing something.

# Development


# Solution:
## Stage 1
* After the video plays and the hint is given, the agent must run the database executable and exploit it to get the email address to connect to the server that began running in the background.
* The database executable allows the agent to enter in sql commands and then displays the results.
```
# First find out what tables are in the database:
SELECT name FROM sqlite_master WHERE type='table';
# Query the data and look through it
SELECT * FROM secret_info;
# Once you try to connect to the server and it sends an error message about needing and email
# you can query for an email in the database
SELECT * FROM secret_info WHERE data LIKE '%@%';
```
* This is how you get the email address
* Then use it to connect to the server, the code for client can be seen in [client.py](client.py)
* The port number was hinted to in the video, the date 10/9/23 when Darwish's predesecor was killed is the only number given. Port number = 10923
* Once you send to the correct email address the server will start sending the pcap file, if you don't catch it on the first round, you will see that in the server's cmd it printed "File sent successfully" so you can see that it is sending a file. You can also see that in wireshark that it is sending and being captured on the loopback. You can reconnect to the server and capture the pcap file.

## Stage 2
* When you open the pcap file you will notice the http post request has in the content type hidden "application/encrypted.code.hamas.aza."
* Check that out, and you will see that in the data section it says "Secret_key=HamasWar" this is the symmetric key
  ![image](https://github.com/user-attachments/assets/9c0664a7-6407-44d2-b453-bc1ec5b6a1a6)

* Then you can will also see many TCP packets, you can click on the stream and see 185 packets were sent.
* Notice in the video it hinted to the fact that they are sending audio file, here this is a wav audio file.
* Reconstruct it using scapy, the code to reconstruct it and get the encrypted message is [here](rebuild_wav.py)
* You will see that it says:  S e c r e t   M e s s a g e   u s i n g   s y m m e t r i c   e n c r y p t i o n ,   T o p   S e c r e t ,   D o   N o t   S h a r e :  #-A.%& IwP[hR^ODfSGqY^V@fQD}U  however, there will be extra spaces in between each letter when reconstructed with scapy, this is given in a hint to remove those spaces.
```
def reconstruct_file_from_pcap(pcap_file, output_file, host='localhost', port=5000):
    packets = rdpcap(pcap_file)

    audio_data = b""
    previous_seq = None

    for pkt in packets:
        # Filter for packets that have both IP and TCP layers
        if pkt.haslayer(IP) and pkt.haslayer(TCP):
            # Check if the packet is destined for the correct host and port
            if pkt[TCP].sport == port:
                # Ensure we only collect in-order data (correct sequence)
                if pkt.haslayer(Raw):  # Check if there's data in this packet
                    tcp_layer = pkt[TCP]
                    #if previous_seq is None or tcp_layer.seq == previous_seq:
                        # Append only the data part of the packet
                    audio_data += pkt[Raw].load
                    previous_seq = tcp_layer.seq + len(pkt[Raw].load)
                   # else:
                    #    print(f"Out of order packet detected with sequence {tcp_layer.seq}")

    # Save the reassembled data to a file
    with open(output_file, 'wb') as f:
        f.write(audio_data)
    print(f"Reconstructed audio file saved as: {output_file}")

# Replace 'your_pcap_file.pcap' with the path to your actual pcap file
# Replace 'reconstructed_audio.wav' with the desired output file name
reconstruct_file_from_pcap('hamas_communications.pcapng', 'reconstructed_audio.wav')

```
* The encryption is with a simple XOR symmetric encryption.
* The code for decrypting is in [msg_decrypt.py](msg_decrypt.py)
* The correct code for entering into the pop-up box is the Lattitude coordinate: 33.71259837310654

## Stage 3
* Now you get a briefing that Hamas has infiltrated DNS servers and is using them to fundraise for their olive grove project.
* Then a warning sounds alerting you of our network infrastructure being infiltrated.
* You need to realize that there is a DNS server and client running in your background and you need to capture the packets in wireshark.
* You will see one site which is being tried to reach is olivetrees.com
* Then if you look at the server's response you will see that it sends back also a weird response including a longitude coordinate: 73.03283493301709
  ![image](https://github.com/user-attachments/assets/32fe8776-678a-48e9-bbf9-28d96250ab74)

* Look up on Google maps to find the location of these coordinates and the final location is: (33.71259837310654, 73.03283493301709) = Islamabad, Pakistan
* The city Darwish is hiding in is Islamabad, and that is the location to enter into the final box.
* Pakistan may be far, but no place is beyond the reach of the long arm of the IDF.

### Mission Accomplished
