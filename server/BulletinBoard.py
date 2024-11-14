class BulletinBoard:
	def __init__(self):
		self.messages = []
		self.members = {}

	def _groupjoin(self, username, conn):
		"""
		adds a user to the group. also needs to send the updated user list to everyone in the group
		"""
		self.members[username] = conn
		pass

	def _grouppost(self, username, message):
		"""
		adds a message to the group. also needs to send the message to everyone in the group
		"""
		pass

	def _groupusers(self, conn):
		"""ß
		gets the list of users in the group and sends it to the user
		"""
		pass

	def _groupleave(self, username):
		"""
		removes the user from the group. also needs to send the updated user list to everyone in the group
		"""
		pass

	def _groupmessage(self, conn, message_id):
		"""
		sends the user the message with the given id
		"""
		pass

	# helper functions start here..
