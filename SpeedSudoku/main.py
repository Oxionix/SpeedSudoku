import socket
import time
import threading
from Client import Client
import Room
import globvar
import Feld

PLAYERCAP = 20
newclients = []

threads = []

port = 12345
s = socket.socket()
print("Socket successfully created")
s.bind(('', port))
print("Socket binded to %s" % (port))
s.listen(PLAYERCAP)
print("Socket is listening")


def exec_msg(soc, addr):
    c1 = Client(soc, addr)
    while True:
        fullmsg = c1.receive_msg()  # Wartet unendlich auf Nachricht
        if fullmsg is None or not fullmsg:
            r = c1.getRoom()
            if r is not None:
                c1.getRoom().c_finished(c1, float('inf'))
            c1.disconnect()
            return
        else:
            # Anweisungen von client ausführen
            print(fullmsg)
            fullmsg = fullmsg.split(":")
            command = fullmsg[0]
            arguments = []
            if len(fullmsg) == 2:
                arguments = fullmsg[1].split(",")
            # print(1, fullmsg)
            # print(2, command)
            # print(3, arguments)
            if command == "login":
                if not arguments[0] in globvar.user_db:
                    print(1)
                    c1.send_msg("login:False,Username or password is wrong")
                elif not globvar.user_db[arguments[0]] == arguments[1]:
                    print(2)
                    c1.send_msg("login:False,Username or password is wrong")
                elif arguments[0] in Client.usern_to_client:
                    print(3)
                    c1.send_msg("login:False,User already logged in")
                else:
                    c1.send_msg("login:True")
                    c1.give_usern(arguments[0])

            elif command == "register":
                usern = arguments[0]
                passw = arguments[1]
                if usern in globvar.user_db:
                    c1.send_msg('register:False,Username already taken')
                else:
                    globvar.user_db[usern] = passw
                    globvar.has_new_user = True
                    c1.send_msg('register:True')
                    c1.give_usern(usern)

            elif command == "makeroom":
                r = Room.Room(c1)
                r.refresh()
            elif command == "joinroom":
                if arguments[0] in Room.Room.code_registry:
                    r = Room.Room.code_registry[arguments[0]]
                    r.AddClient(c1)
                    c1.send_msg("joinroom:True")
                    r.refresh()
                else:
                    c1.send_msg("joinroom:False,Room doesn't exist")
            elif command == "leaveroom":
                c1.getRoom().KickClient(c1)
            elif command == "printroom":
                c1.send_msg(str(c1.getRoom()))
            elif command == "setgame":
                r = c1.getRoom()
                r.setgame(arguments[0])
            elif command == "setdif":
                c1.getRoom().setdif(arguments[0])
            elif command == "startgame":
                c1.getRoom().startgame()
            elif command == "time":
                c1.getRoom().c_finished(c1, float(arguments[0]), arguments[1])


def thread_make_sud():
    timer1 = time.time()
    while True:
        s = 0
        """for i in globvar.sud_db.values():
            s += len(i)
        print(s)"""
        newsud = Feld.Feld.make_sud(3)
        dif = newsud.count_empty()
        if len(globvar.sud_db[dif]) < 100:
            globvar.sud_db[dif].append(newsud)
        if (time.time() - timer1) > 600:
            globvar.write_sud_db()
            timer1 = time.time()
        if (time.time() - timer1) > 100 and globvar.has_new_user:
            globvar.has_new_user = False
            globvar.write_user_db()


globvar.read_sud_db()
globvar.read_user_db()
# print('sub_db:')
# print(globvar.sud_db)
tsud = threading.Thread(target=thread_make_sud)
tsud.start()

while True:
    newsoc, newaddr = s.accept()
    print("new connection")
    t1 = threading.Thread(target=exec_msg, args=(newsoc, newaddr))
    threads.append(t1)
    t1.start()