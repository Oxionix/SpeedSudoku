import random
import Client
import Game


class Room:
    code_registry = {}  # maps codes to room

    def __init__(self, first_client):
        # print("hi")
        self.Clients = [first_client]
        self.admin = first_client
        first_client.join_room(self)
        self.code = self.gen_code()
        self.game = Game.GameSudoku(self)

    def gen_code(self):
        r = random.randint(1000, 9999)
        r = str(r)
        if r not in Room.code_registry.keys():
            Room.code_registry[r] = self
            print(r)
            self.admin.send_msg("makeroom:" + r)
            return r
        else:

            return self.gen_code()

    def __str__(self):
        s = ""
        for i in self.Clients:
            s += str(i) + ";"
        return s[:-1]

    def AddClient(self, c: Client.Client):
        self.Clients.append(c)
        c.join_room(self)
        print(self)
        # return self

    def refresh(self):
        self.send_msg_to_room("user:" + str(self))

    def KickClient(self, c: Client.Client):
        self.Clients.remove(c)
        c.leave_room()
        if not self.Clients:    # Wenn es keine Clients mehr gibt, selbst löschen
            del Room.code_registry[self.code]
            return
        self.refresh()

    def setgame(self, s):   # input as string? changeable
        self.game = Game.GameSudoku(self)

    def send_msg_to_room(self, msg):
        for c in self.Clients:
            c.send_msg(msg)

    def startgame(self):
        if self.game is None:
            pass    # throw an error
        else:
            self.game.start(self.Clients)

    def c_finished(self, c, t, err):
        if not self.game.isstarted():
            return
        else:
            self.game.c_finished(c, t, err)

    def setdif(self, dif):
        self.game.setdif(dif)
