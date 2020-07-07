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
        self.p = self.connect()

    def get_players(self):
        return self.p

    def connect(self):
        self.client.connect(self.address)
        return receive(self.client)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return receive(self.client)
        except socket.error as e:
            print(e)


def receive(client):
    reply = []
    try:
        while True:
            packet = client.recv(1048)
            # print('packet: ', packet)
            if not packet:
                break
            reply.append(packet)
    except socket.error as e:
        pass
    if not reply:
        print('empty reply')
        return
    reply = b"".join(reply)
    # print('reply: ', reply)
    return pickle.loads(reply)
