import socket
import time
def udp_server():
    server_ip = "172.16.81.100"
    server_port=11000
    client_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sequence_number = 0
    while True:
        message = f"Message ke-{sequence_number}".encode()

        client_socket.sendto(message,(server_ip, server_port))
        client_socket.settimeout(2)
        print(f"sent: {message.decode()}")
        # Wait for ACK
        try:
            acknowledgement, _ = client_socket.recvfrom(1024)
            if acknowledgement.decode() == f"Acknowledgement {message.decode()}":
                print(f"received ACK: {sequence_number}")
            else:
                print("invalid ack")
        except socket.timeout:
            print(f"Timeout for message {sequence_number}")
            continue

        sequence_number += 1
        time.sleep(0.05)

def main():
    udp_server()

if __name__ == "__main__":
    main()