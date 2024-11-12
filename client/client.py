import socket
import threading

# client configs
HOST = '127.0.0.1'
PORT = 65432

def receive_messages(sock):
	while True:
		try:
			message = sock.recv(1024).decode('utf-8')
			if not message:
				print("server disconnected")
				break
			else:
				print(message)
		except:
			break

def main():
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((HOST, PORT))

	recieve_thread = threading.Thread(target=receive_messages, args=(client_socket,))
	recieve_thread.start()

	while True:
		command = input()
		if command == "%exit":
			client_socket.sendall("%leave")
			break
		client_socket.sendall(command.encode('utf-8'))
	client_socket.close()

if __name__ == "__main__":
	main()