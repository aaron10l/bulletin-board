from datetime import datetime
class BulletinBoard:
	def __init__(self):
		self.messages = []
		self.members = {} # username: conn

	def _groupjoin(self, username, conn):
		"""
		adds a user to the group. also needs to send the updated user list to everyone in the group
		"""
		self.members[username] = conn

	def _grouppost(self, username, subject, message):
		"""
		adds a message to the group. also sends the message to everyone in the group
		"""
		if username not in self.members:
			raise PermissionError(f"User '{username}' is not a member of this group.")

		post_id = len(self.messages) + 1
		post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		post = f"{post_id}, {username}, {post_date}, {subject}, {message}"
		post_thumbnail = f"{post_id}, {username}, {post_date}, {subject}"
		self.messages.append(post)
		for user, conn in self.members.items():
			try:
				conn.sendall(post_thumbnail.encode('utf-8'))
			except Exception as e:
				print(f"Failed to send message to {user}: {e}")

	def _groupusers(self, username=None):
		"""
		gets the list of users in the group and sends it to the user. if no user is provided send to all members.
		"""
		user_list = ', '.join(self.members.keys())
		if not username:
			for user, conn in self.members.items():
				conn.sendall(f"users: {user_list}".encode('utf-8'))
		else:
			conn = self.members[username]
			conn.sendall(f"users: {user_list}".encode('utf-8'))

	def _groupleave(self, username):
		"""
		removes the user from the group. also needs to send the updated user list to everyone in the group
		"""
		del self.members[username]

	def _groupmessage(self, username, message_id):
		"""
		sends the user the message with the given id
		"""
		message_index = int(message_id) - 1
		if 0 <= message_index < len(self.messages):
			conn = self.members[username]
			conn.sendall(self.messages[message_index].encode('utf-8'))
		else:
			conn = self.members[username]
			conn.sendall(f"message not found, should be in the range 1 - {len(self.messages)}, inclusive.\n".encode('utf-8'))

	# helper functions start here..

	def _send_prev_two_messages(self, username):
		"""
		sends the user the previous two messages. if less than two messages, send all available messages
		"""

		conn = self.members[username]
		if len(self.messages) >= 2:
			conn.sendall(self.messages[len(self.messages) - 2].encode('utf-8'))
			conn.sendall(self.messages[len(self.messages) - 1].encode('utf-8'))
		elif len(self.messages) == 1:
			conn.sendall(self.messages[0].encode('utf-8'))
