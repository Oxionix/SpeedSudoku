import socket
import time

s = socket.socket()


class Server:
    def __init__(self, ip_address, port):
        self.ip = ip_address
        self.port = port

    def connect_to(self):
        s.connect((str(self.ip), int(self.port)))

    def receive_msg(self):
        msg = s.recv(1024).decode()
        return msg

    def send_msg(self, msg):
        msg = str(msg)
        s.send(msg.encode())

    def close_con(self):
        s.close()