import socket

SERVER_ADDRESS = "localhost"
PORT = 5000


def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_ADDRESS, PORT))
    sock.listen(1)

    while True:
        print(f"Waiting for client connection on {SERVER_ADDRESS}:{PORT}")
        client_socket, client_address = sock.accept()
        print(f"Client connected from {client_address[0]}:{client_address[1]}")
        # Handle client connection

