import socket
import pickle
from globe import *

# TODO - massive amount of data needs to be received (entire list of points)
# TODO - get_heads()


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(0.05)
        self.server = SERVER
        self.port = PORT
        self.address = (self.server, self.port)
        self.client.connect(self.address)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(f"send {e}")

    def receive(self):
        try:
            return receive(self.client)
        except socket.error as e:
            print(f"recv {e}")


def receive(client):
    reply = []
    try:
        while True:
            packet = client.recv(2048)
            # print('packet: ', packet)
            if not packet:
                break
            reply.append(packet)
    except socket.error as e:
        print(f"receive {e}")

    if not reply:
        return

    reply = b"".join(reply)
    reply = pickle.loads(reply)

    return reply
