import socket
import pickle
from globe import *


# TODO - massive amount of data needs to be received (entire list of points)
# TODO - get_heads()


class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.settimeout(0.015)
		self.server = SERVER
		self.port = PORT
		self.address = (self.server, self.port)
		self.client.connect(self.address)
	
	def send(self, data):
		try:
			self.client.send(pickle.dumps(data))
		except socket.error as e:
			pass
	
	def receive(self):
		reply = []
		try:
			while True:
				packet = self.client.recv(1042)
				if not packet:
					break
				reply.append(packet)
		except socket.error as e:
			pass
		
		if not reply:
			return
		
		reply = b"".join(reply)
		reply = pickle.loads(reply)
		return reply
