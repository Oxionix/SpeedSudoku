import threading
import globvar

globvar.serv.connect_to()

def recfunc():
    while True:
        fullmsg = globvar.serv.receive_msg()
        if fullmsg == None:
            pass
            # server disconnected
        else:
            print(fullmsg)
            fullmsg = fullmsg.split(":")
            command = fullmsg[0]
            arguments = []
            if len(fullmsg) == 2:
                arguments = fullmsg[1].split(",")
            if command == "login":
                globvar.a.fr.handleresponse(arguments)
            elif command == "register":
                globvar.a.fr.handleresponse(arguments)
            elif command == "makeroom":
                globvar.a.fr.handleresponse_mroom(arguments)
            elif command == "joinroom":
                globvar.a.fr.handleresponse_jroom(arguments)
            elif command == "user":
                globvar.a.fr.refresh_user(arguments)
            elif command == "sudoku":
                globvar.a.fr.handleresponse(arguments)
            elif command == "finished":
                globvar.a.fr.handleresponsefin(arguments)
            elif command == "currentstandings":
                globvar.a.fr.handleresponse(arguments)



def login(args):
    if args[0] == "True":
        globvar.logreg = True            # can also be a propety/variable of GUI page/frame  (instead of logreg)
    else:
        globvar.logreg = False
def register(args):
    if args[0] == "True":
        globvar.logreg = True
    else:
        globvar.logreg = False
def room(args):
    pass
def sudoku(args):
    pass
def finished(args):
    pass




t1 = threading.Thread(target=recfunc)
t1.daemon = True
t1.start()
globvar.a.start()
quit()


