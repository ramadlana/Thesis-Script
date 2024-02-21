import socket
def udp_server():
    server_ip = "172.16.81.100"
    server_port=11000
    client_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sequence_number = 0
    udp_dropped = 0
    while (sequence_number < 1000):
        message = f"UDP Datagram ke-{sequence_number}".encode()

        client_socket.sendto(message,(server_ip, server_port))
        client_socket.settimeout(1)

        # Wait for ACK
        try:
            acknowledgement, _ = client_socket.recvfrom(1024)
            if acknowledgement.decode() == f"Acknowledgement {message.decode()}":
                print(f"{acknowledgement.decode()}")
            else:
                print("invalid ack")
            sequence_number += 1
        except socket.timeout:
            udp_dropped += 1
            print(f"!!!!!!!!!!!!!!! UDP Datagram ke-{sequence_number} Gagal diterima peer !!!!!!!!!!")
            sequence_number += 1
            continue
    print("total datagram drop: ",udp_dropped)
    print("total datagram dikirim: ", sequence_number)
def main():
    udp_server()

if __name__ == "__main__":
    main()