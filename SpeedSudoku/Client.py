class Client:
    usern_to_client = {}
    client_to_usern = {}

    def __init__(self, soc, ip_address):
        self.soc = soc
        self.ip = ip_address
        self.usern = None
        self.room = None

    def getRoom(self):
        return self.room

    def give_usern(self, usern):
        self.usern = usern
        Client.usern_to_client[usern] = self
        Client.client_to_usern[self] = usern

    def disconnect(self):
        try:
            print("disconnected")
            Client.client_to_usern.pop(self)
            Client.usern_to_client.pop(self.usern)
            if self.room is not None:
                self.room.KickClient(self)
        except KeyError:
            pass

    def join_room(self, r):
        self.room = r

    def leave_room(self):   # only access from KickClient pls
        self.room = None

    def receive_msg(self):
        try:
            msg = self.soc.recv(1024).decode()
            return msg
        except:
            return None

    def send_msg(self, msg):
        try:
            msg = str(msg)
            self.soc.send(msg.encode())
        except ConnectionResetError:
            print("Connection wurde schon geschlossen")

    def is_connected(self):
        try:
            self.send_msg('areyoucon')
            return True
        except:
            return False

    def close_con(self):
        self.soc.close()

    def __str__(self):
        return self.usern

    def __repr__(self):
        return "Client: " + self.usern