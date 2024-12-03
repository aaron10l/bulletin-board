import socket
import threading
import json

def receive_messages(sock):
	"""
	continuously reads messages from the server and prints output on client side
	"""
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
	"""
	this function runs continuously and it's main purpose is to parse the text the user types, 
	and format it in a json-like way to send it to the server. this ensures that we stop errors before they
	even reach the server.

	this is basically the format of every request sent to the server:
	{
		"command": ...,
		"command specific fields (group, message, subject, etc...)": ...,
	}
	"""
	client_socket = None
	while True:
		# parsing the command the user types
		command = input("> ")
		command_args = command.split()

		# matching the first command argument (should be the command) to one of the possible request types
		# to be sent to the server
		if not command_args:
			print("no valid command found")
			continue
		elif command_args[0] == "%connect":
			if len(command_args) != 3:
				print("usage: %connect <host> <port>")
				continue
			HOST, PORT = str(command_args[1]), int(command_args[2])
			# attempting to connect to the server and spawns off a new thread that recieves messages from the server. 
			# note that this thread runs on the CLIENT side.
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
				print("usage: %post ; subject ; <message>")
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
		elif command_args[0] == "%groups":
			request = {"command": "%groups"}
			client_socket.sendall(json.dumps(request).encode('utf-8'))
		elif command_args[0] == "%groupjoin":
			if len(command_args) != 2:
				print("usage: %groupjoin <group_name>")
				continue
			request = {"command": "%groupjoin", "group": command_args[1]}
			client_socket.sendall(json.dumps(request).encode('utf-8'))
		elif command_args[0] == "%grouppost":
			post_command_args = command.split(";")
			if len(post_command_args) != 4:
				print("usage: %grouppost ; <groupname> ; <subject> ; <message>")
				continue
			request = {"command": "%grouppost", "group": post_command_args[1].strip(), "subject": post_command_args[2].strip(), "message": post_command_args[3].strip()}
			client_socket.sendall(json.dumps(request).encode('utf-8'))
		elif command_args[0] == "%groupusers":
			if len(command_args) != 2:
				print("usage: %groupusers <group_name>")
				continue
			request = {"command": "%groupusers", "group": command_args[1]}
			client_socket.sendall(json.dumps(request).encode('utf-8'))
		elif command_args[0] == "%groupleave":
			if len(command_args) != 2:
				print("usage: %groupleave <group_name>")
				continue
			request = {"command": "%groupleave", "group": command_args[1]}
			client_socket.sendall(json.dumps(request).encode('utf-8'))
		elif command_args[0] == "%groupmessage":
			if len(command_args) != 3:
				print("usage: %groupmessage <group_name> <message_id>")
				continue
			request = {"command": "%groupmessage", "group": command_args[1], "message_id": int(command_args[2])}
			client_socket.sendall(json.dumps(request).encode('utf-8'))
		else:
			# handling username being sent (when initializing a new user)
			client_socket.sendall(command.encode('utf-8'))



if __name__ == "__main__":
	run()
