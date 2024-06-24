import socket

def udp_server():
    server_ip = "172.16.81.100"
    server_port = 11000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, server_port))

    print(f"Server listening on {server_ip}:{server_port}")

    while True:
        message, client_address = server_socket.recvfrom(9000)
        received_message = message.decode()
        print(f"Received message from {client_address}: {received_message}")
        
        # Construct the acknowledgment message
        ack_message = f"Acknowledgement {received_message}"
        print(f"Sending ACK to {client_address}: {ack_message}\n\n")
        server_socket.sendto(ack_message.encode(), client_address)

if __name__ == "__main__":
    udp_server()
