import socket

def udp_server():
    server_ip = "172.16.81.100"
    server_port=11000
    server_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip,server_port))
    print("UDP server listening on port 11000")
    while True:
        data, client_address = server_socket.recvfrom(1024)
        print(f"received message from {client_address}: {data.decode()}")

        #send ack
        acknowledgement = f"Acknowledgement {data.decode()}".encode()
        server_socket.sendto(acknowledgement, client_address)
def main():
    udp_server()

if __name__ == "__main__":
    main()