import socket
import string
import random

def generate_random_data(size):
    char = string.ascii_letters + string.digits
    return "".join(random.choice(char) for _ in range(size))

def udp_client():
    server_ip = "172.16.81.100"
    server_port = 11000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sequence_number = 0
    udp_dropped = 0
    while sequence_number < 1000:
        voice_data_dummy = generate_random_data(8*1024)  # generate 8KB data
        message = f"UDP Datagram ke-{sequence_number} - {voice_data_dummy}"
        encoded_message = message.encode()

        #print(f"Sending message: {message}")
        client_socket.sendto(encoded_message, (server_ip, server_port))
        client_socket.settimeout(1)

        # Wait for ACK
        try:
            acknowledgement, _ = client_socket.recvfrom(9000)
            received_ack = acknowledgement.decode()
            expected_ack = f"Acknowledgement {message}"
            
            if received_ack == expected_ack:
               print(f"Received correct ACK: {received_ack} \n\n")
            else:
                print(f"Invalid ACK")
            
            sequence_number += 1
        except socket.timeout:
            udp_dropped += 1
            print(f"!!!!!!!!!!!!!!! UDP Datagram ke-{sequence_number} Gagal diterima peer !!!!!!!!!!")
            sequence_number += 1
            continue
    print("Total datagram drop:", udp_dropped)
    print("Total datagram dikirim:", sequence_number)

def main():
    udp_client()

if __name__ == "__main__":
    main()
