import Feld
import globvar
import random


class GameSudoku:
    def __init__(self, r):      # r = Room (zum Senden)
        self.r = r
        self.dif = None
        self.started = False
        self.clients = None
        self.clients_times = None

    def setdif(self, dif):
        self.dif = dif

    def isstarted(self):
        return self.started

    def start(self, Clients):
        if self.dif is None:
            pass    # throw an error
        elif self.started:
            pass    # throw an error
        self.started = True
        self.clients = Clients
        self.clients_times = {}
        f = GameSudoku.getSudoku(self.dif)

        self.r.send_msg_to_room("sudoku:" + f.strv2() + "," + str(f.getbase()))

    def c_finished(self, c, t, err):     # client, time
        if not self.started:
            pass    # throw an error
        self.clients_times[c] = t, err
        s = "currentstandings:"
        for c in self.clients_times.keys():
            s += str(c) + " "
            s += str(self.clients_times[c][0]) + " "
            s += str(self.clients_times[c][1]) + ";"
        s = s.strip(";")
        for c in self.clients_times.keys():
            c.send_msg(s)

        if len(self.clients_times) == len(self.clients):
            self.end()

    def end(self):
        ranking = sorted(self.clients_times, key=self.clients_times.get)
        print(self.clients_times)
        print(ranking)
        msg = ""
        for count, c in enumerate(ranking):
            print(c)
            t = self.clients_times[c][0]
            msg += str(count) + ". " + str(c) + " Zeit: " + str(t) + "sek\n"    # DO NOT SEND ":"!!!!
            # self.r.send_msg_to_room(str(count) + ". " + str(c) + " Zeit: " + str(t) + "sek")
        self.r.send_msg_to_room(msg)
        self.started = False
        self.clients = None
        self.clients_times = None

    @staticmethod
    def getSudoku(dif):
        # translate dif to empty spaces
        grenzen = list(globvar.difs.values())
        print(grenzen)
        grenze = globvar.difs[dif]
        grenzen.sort()
        links = grenze
        rechts = 81
        if grenzen[-1] == grenze:
            rechts = 81
        else:
            rechts = grenzen[grenzen.index(grenze)+1]
            # print(grenzen.index(grenze))
        # print(links, rechts)
        # get Sud from database
        possible = []
        for i in range(links, rechts):
            if len(globvar.sud_db[i]) > 0:
                possible.append(i)

        r = random.choice(possible)
        f = globvar.sud_db[r].pop()

        return f

