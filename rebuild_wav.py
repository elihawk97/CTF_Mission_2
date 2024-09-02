from scapy.all import *
from scapy.layers.inet import TCP, IP

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
