import socket
import threading
import json

def receive_messages(sock):
	while True:
		try:
			message = sock.recv(1024).decode('utf-8')
			if not message:
				print("server disconnected")
				break
			else:
				print("\r" + message + "\n> ", end="")
		except:
			break

def run():
	client_socket = None
	while True:
		command = input("> ")
		command_args = command.split()
		if command_args[0] == "%connect":
			if len(command_args) != 3:
				print("usage: %connect <host> <port>")
				continue
			HOST, PORT = str(command_args[1]), int(command_args[2])
			try:
				client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				client_socket.connect((HOST, PORT))
				print(f"connected to {HOST} on port {PORT}")
				recieve_thread = threading.Thread(target=receive_messages, args=(client_socket,))
				recieve_thread.start()
			except:
				print("could not connect to server")
		elif command_args[0] == "%join":
			if len(command_args) != 1:
				print("usage: %join")
				continue
			request = {"command": "%groupjoin", "group": "default"}
			client_socket.sendall(json.dumps(request).encode('utf-8'))
		elif command_args[0] == "%post":
			post_command_args = command.split(";")
			if len(post_command_args) != 3:
				print("usage: %post ; subject ; <message> ; ")
				continue
			request = {"command": "%grouppost", "group": "default", "subject": post_command_args[1].strip(), "message": post_command_args[2].strip()}
			client_socket.sendall(json.dumps(request).encode('utf-8'))
		elif command_args[0] == "%users":
			if len(command_args) != 1:
				print("usage: %users")
				continue
			request = {"command": "%groupusers", "group": "default"}
			client_socket.sendall(json.dumps(request).encode('utf-8'))
		elif command_args[0] == "%leave":
			if len(command_args) != 1:
				print("usage: %leave")
				continue
			request = {"command": "%groupleave", "group": "default"}
			client_socket.sendall(json.dumps(request).encode('utf-8'))
		elif command_args[0] == "%message":
			if len(command_args) != 2:
				print("usage: %message <message_id>")
				continue
			request = {"command": "%groupmessage", "group": "default", "message_id": int(command_args[1].strip())}
			client_socket.sendall(json.dumps(request).encode('utf-8'))
		elif command_args[0] == "%exit":
			request = {"command": "%exit"}
			client_socket.sendall(json.dumps(request).encode('utf-8'))
			client_socket.close()
			break
		else:
			# username being sent
			client_socket.sendall(command.encode('utf-8'))



if __name__ == "__main__":
	run()