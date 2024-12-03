import socket
import threading
from BulletinBoard import BulletinBoard
import json

class Server:
	"""
    A server implementation for managing multiple bulletin board groups.
    Handles:
	- User connections
	- Group management
	- Message broadcasting
    """
	def __init__(self):
		"""
		Initialize some default bulletin boards where each group is an instance
		of the BulletinBoard class
		"""
		self.bulletinboards = {"default": BulletinBoard(),
								 "group1": BulletinBoard(),
								"group2": BulletinBoard(),
								"group3": BulletinBoard(),
								"group4": BulletinBoard(),
								"group5": BulletinBoard()}

	def run(self):
		"""
        - Start server to listen for incoming client connections.
        - Spawns a new thread for each client to handle their requests.
        """
		# Server configurations
		HOST = '127.0.0.1'
		PORT = 65432

		# starting server on given socket
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind((HOST, PORT))
		server_socket.listen()
		print(f"server started on host {HOST} and port {PORT}")

		# Continuously listening for new connections
		while True:
			conn, addr = server_socket.accept()
			print(f"connected to {addr}")

			# Handle the client connection in a new thread
			thread = threading.Thread(target=self.handle_client, args=(conn,))
			thread.start()

	def handle_client(self, conn):
		"""
        - Handles communication with connected client.
        - Processes user commands and routes them to appropriate bulletin board.

        Handles:
            %groupjoin, %grouppost, %groupusers, %groupleave, %groupmessage, %exit, %groups
        """

		# Handle username input
		conn.sendall(b"Enter a username: \n")
		username = conn.recv(1024).decode('utf-8').strip()

		# checking if the new username already exists anywhere
		for group in self.bulletinboards:
			for member in self.bulletinboards[group].members:
				if member == username:
					conn.sendall(b"username already exists, please choose another username: \n")
					username = conn.recv(1024).decode('utf-8').strip()
		
		# Main loop to process client requests
		while True:
			try:
				# recieve requests from the client and print them on server side for logging
				request = conn.recv(1024).decode('utf-8').strip()
				request = json.loads(request)
				print(f"recieved request : {request}")

				# defining command endpoints. notice that most of the part 1 commands can be handled using the endpoint from part 2,
				# by just using a default value.
				match request["command"]:
					case "%groupjoin":
						"""
						attempts to add the user to the requested group, and sends the group users as well as prev. two messages
						"""
						try:
							self.bulletinboards[request["group"]]._groupjoin(username, conn)
							self.bulletinboards[request["group"]]._groupusers()
							self.bulletinboards[request["group"]]._send_prev_two_messages(username)
						except PermissionError as e:
							conn.sendall(f"Error: {str(e)}\n".encode('utf-8'))
						except KeyError:
							group = request["group"]
							conn.sendall(f"Error: Group '{group}' does not exist.\n".encode('utf-8'))
					case "%grouppost":
						"""
						attempts to add a post to the specified group. the sending of the message to each user in the group is handled
						in _grouppost()
						"""
						try:
							group = request["group"]
							subject = request["subject"]
							message = request["message"]
							self.bulletinboards[request["group"]]._grouppost(username, subject, message)
						except PermissionError as e:
							conn.sendall(f"Error: {str(e)}\n".encode('utf-8'))
						except KeyError:
							conn.sendall(f"Error: Group '{group}' does not exist.\n".encode('utf-8'))
					case "%groupusers":
						"""
						sends the list of users in the group to the requesting user.
						"""
						group = request["group"]
						self.bulletinboards[group]._groupusers(username)
					case "%groupleave":
						"""
						attempts to remove the user from the requested group, and sends the new user list to all users.
						"""
						try:
							group = request["group"]
							self.bulletinboards[group]._groupleave(username)
							self.bulletinboards[group]._groupusers()
						except PermissionError as e:
							conn.sendall(f"Error: {str(e)}\n".encode('utf-8'))
						except KeyError:
							conn.sendall(f"Error: Group '{group}' does not exist.\n".encode('utf-8'))
					case "%groupmessage":
						"""
						attempts to send a message to each member in the requested group.
						"""
						try:
							group = request["group"]
							message_id = request["message_id"]
							self.bulletinboards[group]._groupmessage(username, message_id)
						except PermissionError as e:
							conn.sendall(f"Error: {str(e)}\n".encode('utf-8'))
						except KeyError:
							conn.sendall(f"Error: Group '{group}' does not exist.\n".encode('utf-8'))
					case "%exit":
						"""
						removes the exiting user from each group they are in.
						"""
						for group in self.bulletinboards:
							if username in self.bulletinboards[group].members:
								self.bulletinboards[group]._groupleave(username)
					case "%groups":
						"""
						sends the list of joinable groups to the requesting user.
						"""
						groups = ', '.join(self.bulletinboards.keys())
						conn.sendall(f"available groups: {groups}".encode('utf-8'))

			except:
				# Handle abrupt disconnection or invalid input
				break

if __name__ == "__main__":
	# Initialize and run the server
	server = Server()
	server.run()
