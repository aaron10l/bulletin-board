import socket
import threading
from datetime import datetime
from BulletinBoard import BulletinBoard
import json

class Server:
	def __init__(self):
		self.bulletinboards = {"default": BulletinBoard(),
								 "group1": BulletinBoard(),
								"group2": BulletinBoard(),
								"group3": BulletinBoard(),
								"group4": BulletinBoard(),
								"group5": BulletinBoard()}

	def run(self):
		# server configs
		HOST = '127.0.0.1'
		PORT = 65432

		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind((HOST, PORT))
		server_socket.listen()
		print(f"server started on host {HOST} and port {PORT}")

		while True:
			conn, addr = server_socket.accept()
			print(f"connected to {addr}")

			thread = threading.Thread(target=self.handle_client, args=(conn,))
			thread.start()

	def handle_client(self, conn):
		# handling %connect
		conn.sendall(b"Enter a username: \n")
		username = conn.recv(1024).decode('utf-8').strip()

		for group in self.bulletinboards:
			for member in self.bulletinboards[group].members:
				if member == username:
					conn.sendall(b"username already exists, please choose another username: \n")
					username = conn.recv(1024).decode('utf-8').strip()
		
		while True:
			try:
				request = conn.recv(1024).decode('utf-8').strip()
				request = json.loads(request)
				print(f"recieved request : {request}")
				match request["command"]:
					case "%groupjoin":
						self.bulletinboards[request["group"]]._groupjoin(username, conn)
						self.bulletinboards[request["group"]]._groupusers()
						self.bulletinboards[request["group"]]._send_prev_two_messages(username)
					case "%grouppost":
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
						group = request["group"]
						self.bulletinboards[group]._groupusers(username)
					case "%groupleave":
						group = request["group"]
						self.bulletinboards[group]._groupleave(username)
						self.bulletinboards[group]._groupusers()
					case "%groupmessage":
						try:
							group = request["group"]
							message_id = request["message_id"]
							self.bulletinboards[group]._groupmessage(username, message_id)
						except PermissionError as e:
							conn.sendall(f"Error: {str(e)}\n".encode('utf-8'))
						except KeyError:
							conn.sendall(f"Error: Group '{group}' does not exist.\n".encode('utf-8'))
					case "%exit":
						for group in self.bulletinboards:
							if username in self.bulletinboards[group].members:
								self.bulletinboards[group]._groupleave(username)
					case "%groups":
						groups = ', '.join(self.bulletinboards.keys())
						conn.sendall(f"avaliable groups: {groups}".encode('utf-8'))

			except:
				break

if __name__ == "__main__":
	server = Server()
	server.run()
	
# TODO:
# block users from sending a message to a group they aren't in
# add functionality to show users prev 2 messages when they join a group
# debug everything
