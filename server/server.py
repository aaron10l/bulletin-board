import socket
import threading

# server configs
HOST = '127.0.0.1'
PORT = 65534

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"server started on host {HOST} and port {PORT}")

    while True:
        conn, addr = server.accept()
        print(f"client requested connection: {conn}, {addr}")

if __name__ == "__main__":
    main()
