import tkinter as tk
from globvar import serv
import globvar
import time
from copy import deepcopy
import Feld
import Solver


smatrix = [[0, 1, 6, 1, 7, 1, 7, 1, 7],
           [5, 1, 6, 1, 7, 1, 7, 1, 1],
           [4, 1, 6, 1, 5, 1, 2, 1, 1],
           [4, 1, 6, 1, 6, 1, 2, 1, 1],
           [4, 1, 4, 1, 6, 1, 2, 1, 1],
           [4, 1, 4, 1, 6, 1, 2, 1, 1],
           [4, 1, 4, 1, 6, 1, 2, 1, 1],
           [4, 1, 4, 1, 7, 1, 2, 1, 1],
           [4, 1, 4, 1, 7, 1, 2, 1, 1],]


class LeaderboardPage(tk.Frame):
    def __init__(self, master, starttime):
        super().__init__(master)

        self.isfinished = False
        self.starttime = starttime

        #print(self.master.winfo_width() / 6, self.master.winfo_width() * 4 / 6)
        self.rechts = tk.Frame(self, width=int(self.master.winfo_width() / 6), height=int(self.master.winfo_height() * 3 / 4),
                               bg="lightgrey")
        self.links = tk.Frame(self, width=int(self.master.winfo_width() * 3 / 6), height=int(self.master.winfo_height() * 3 / 4),
                              bg="lightgrey")
        self.linkslinks = tk.Frame(self, width=int(self.master.winfo_width() / 6),
                              height=int(self.master.winfo_height() * 3 / 4),
                              bg="grey")
        self.mitte = tk.Frame(self, width=int(self.master.winfo_width() / 6),
                              height=int(self.master.winfo_height() * 3 / 4),
                              bg="darkgrey")
        self.oben = tk.Frame(self, width=int(self.master.winfo_width()),
                              height=int(self.master.winfo_height() / 4),
                              bg="black")

        self.rechts.pack_propagate(False)
        self.mitte.pack_propagate(False)
        self.links.pack_propagate(False)
        self.linkslinks.pack_propagate(False)
        self.oben.pack_propagate(False)

        self.rechts.grid_propagate(False)
        self.mitte.grid_propagate(False)
        self.links.grid_propagate(False)
        self.linkslinks.grid_propagate(False)
        self.oben.grid_propagate(False)

        self.linkslinks.grid(column=0, row=1)
        self.links.grid(column=1, row=1)
        self.mitte.grid(column=2, row=1)
        self.rechts.grid(column=3, row=1)
        self.oben.grid(row=0, columnspan=4)

        self.title1 = tk.Label(self.oben, text="Waiting for other players...", font=('Courier', 40), bg='black', fg='white')
        self.title1.place(relx=0.5, rely=0.3, anchor='center')
        self.title2 = tk.Label(self.oben, text="Current Leaderboard", font=('Courier', 35, 'bold'), bg='black', fg='white')
        self.title2.place(relx=0.5, rely=0.7, anchor='center')

        spacer1 = tk.Label(self.linkslinks, bg='grey', font=("Courier", 1))
        spacer1.pack()
        spacer2 = tk.Label(self.links, bg='lightgrey', font=("Courier", 1))
        spacer2.pack()
        spacer3 = tk.Label(self.mitte, bg='darkgrey', font=("Courier", 1))
        spacer3.pack()
        spacer4 = tk.Label(self.rechts, bg='lightgrey', font=("Courier", 1))
        spacer4.pack()
        self.coltitle1 = tk.Label(self.linkslinks, text="Rank", font=('Courier', 27, 'bold'), bg='grey')
        self.coltitle2 = tk.Label(self.links, text="Name", font=('Courier', 27, 'bold'), bg='lightgrey')
        self.coltitle3 = tk.Label(self.mitte, text="Time", font=('Courier', 27, 'bold'), bg='darkgrey')
        self.coltitle4 = tk.Label(self.rechts, text="Mistakes", font=('Courier', 27, 'bold'), bg='lightgrey')
        self.coltitle1.pack()
        self.coltitle2.pack()
        self.coltitle3.pack()
        self.coltitle4.pack()
        spacer1 = tk.Label(self.linkslinks, bg='grey', font=("Courier", 10))
        spacer1.pack()
        spacer2 = tk.Label(self.links, bg='lightgrey', font=("Courier", 10))
        spacer2.pack()
        spacer3 = tk.Label(self.mitte, bg='darkgrey', font=("Courier", 10))
        spacer3.pack()
        spacer4 = tk.Label(self.rechts, bg='lightgrey', font=("Courier", 10))
        spacer4.pack()

        self.timer = tk.Label(self.oben, bg='black', fg='grey', font=("Courier", 25))
        self.timer.place(relx=0.9, rely=0.8, anchor='center')

        self.handleresponse("Fabian 2:45 7;Danny 3:30 2;Nam - -")
        #self.handleresponsefin("Fabian 2:45 7;Danny 3:30 2;Nam 4:20 3")
        self.update_clock()

    def update_clock(self):
        if self.isfinished:
            return
        t1 = time.time()
        t2 = self.starttime
        t3 = str(t1 - t2)
        print(t2)
        print(t3)
        # print(t3)
        t4 = t3
        checklen = t3.split('.')
        digs = len(checklen[0])
        num = 2 + digs
        timestr = t4[:num]
        self.timer.configure(text=timestr)
        self.master.after(100, self.update_clock)

    def handleresponse(self, arguments):
        users = arguments.split(";")
        values = list(map(lambda x: x.split(" "), users))
        self.display_user(values)


    def handleresponsefin(self, arguments):
        self.isfinished = True
        users = arguments.split(";")
        values = list(map(lambda x: x.split(" "), users))
        self.title1.configure(text='Game finished!')
        self.title2.configure(text='Final Leaderboard')
        self.homebut = tk.Button(self.oben, text="🔙", width=3, font=("Courier", 35), bg='yellow', command=self.back)
        self.homebut.place(relx=0, rely=0)
        self.display_user(values)


    def back(self):
        self.master.switch_frame(RoomPage, globvar.rcode)


    def display_user(self, alluserlist):
        for w in self.rechts.winfo_children()[3:]:
            w.destroy()
        for w in self.mitte.winfo_children()[3:]:
            w.destroy()
        for w in self.links.winfo_children()[3:]:
            w.destroy()
        for w in self.linkslinks.winfo_children()[3:]:
            w.destroy()

        for u in range(len(alluserlist)):

            if alluserlist[u][1] == "-":
                l1 = tk.Label(self.linkslinks, text="Playing", font=("Courier", 25), bg='grey')  # rank
            else:
                l1 = tk.Label(self.linkslinks, text=str(u + 1) + ".", font=("Courier", 25), bg='grey') # rank
            l1.pack()

            l2 = tk.Label(self.links, text=alluserlist[u][0], font=("Courier", 25), bg='lightgrey') # name
            l2.pack()

            l3 = tk.Label(self.mitte, text=alluserlist[u][1], font=("Courier", 25), bg='darkgrey') # time
            l3.pack()

            l4 = tk.Label(self.rechts, text=alluserlist[u][2], font=("Courier", 25), bg='lightgrey') # errors
            l4.pack()

            spacer1 = tk.Label(self.linkslinks, bg='grey', font=("Courier", 1))
            spacer1.pack()
            spacer2 = tk.Label(self.links, bg='lightgrey', font=("Courier", 1))
            spacer2.pack()
            spacer3 = tk.Label(self.mitte, bg='darkgrey', font=("Courier", 1))
            spacer3.pack()
            spacer4 = tk.Label(self.rechts, bg='lightgrey', font=("Courier", 1))
            spacer4.pack()



class SudokuPage(tk.Frame):
    def __init__(self, master, sudokumatrix, room):
        super().__init__(master)
        self.sudokumatrix = sudokumatrix
        self.isfinished = False
        self.room = room
        self.errors = 0

        self.c = tk.Canvas(self, height=720, width=720, bg='white',)
        self.c.place(relx=0.05, rely=0.05)
        for i in range(0, 720, 80):
            self.c.create_line([(i, 0), (i, 720)], tag='grid_line')
            if i == 240 or i == 480:
                self.c.create_line([(i-1, 0), (i-1, 720)], tag='grid_line')
                self.c.create_line([(i+1, 0), (i+1, 720)], tag='grid_line')
        for i in range(0, 720, 80):
            self.c.create_line([(0, i), (720, i)], tag='grid_line')
            if i == 240 or i == 480:
                self.c.create_line([(0, i-1), (720, i-1)], tag='grid_line')
                self.c.create_line([(0, i+1), (720, i+1)], tag='grid_line')
        self.textfields = {}

        self.done = tk.Button(self, text='Finished', command=self.finished, width=10, font=("Courier", 40), bg="YELLOW")
        self.done.place(relx=0.67, rely=0.45)

        self.timer = tk.Label(self, text='0.0', font=("Courier", 40))
        self.timer.place(relx=0.85, rely=0.2, anchor='e')
        self.starttime = time.time()

        ly = 0
        lx = 0
        for y in range(40, 720, 80):
            for x in range(40, 720, 80):
                if self.sudokumatrix[ly][lx] == 0:
                    e1 = tk.Text(width=1, height=1, font=('Arial', 45), borderwidth=0, foreground='blue')
                    self.textfields[(ly, lx)] = e1
                    e1.tag_configure("center", justify="center")
                    e1.tag_configure("bold", )
                    e1.tag_add("center", "1.0", "end")
                    self.c.create_window(x, y, window=e1)
                else:
                    num = str(self.sudokumatrix[ly][lx])
                    e2 = tk.Label(text=num, font=('Arial', 45), width=1, background='white')
                    self.c.create_window(x, y, window=e2)
                lx += 1
            ly += 1
            lx = 0

        self.update_clock()

    def finished(self):
        self.isfinished = True
        self.master.switch_frame(LeaderboardPage, self.starttime) #############################################################
        serv.send_msg("time:" + str(self.timestr) + "," + str(self.errors))
        return
        dic = self.textfields
        solved = deepcopy(self.sudokumatrix)

        for key, value in dic.items():
            val = value.get("1.0","end-1c")
            if len(val) > 0:
                solved[key[0]][key[1]] = int(val[-1])
            else:
                solved[key[0]][key[1]] = 0



        f = Feld.Feld(solved, 3)
        solution = Solver.Solver.solve(f)
        counter = 0
        for key, value in solved.items():
            pass
        self.master.switch_frame(RoomPage, 0, self.room)
        # self.destroy()
        # self.master.fr = self.room
        # self.master.fr.pack(fill="both", expand="yes")

    def update_clock(self):
        if self.isfinished:
            return
        t1 = time.time()
        t2 = self.starttime
        t3 = str(t1 - t2)
        # print(t3)
        t4 = t3
        checklen = t3.split('.')
        digs = len(checklen[0])
        num = 2 + digs
        self.timestr = t4[:num]
        self.timer.configure(text=self.timestr)
        self.master.after(100, self.update_clock)


class RoomPage(tk.Frame):
    def __init__(self, master, rcode, room=None):
        super().__init__(master)
        self.rcode = rcode
        globvar.rcode = self.rcode
        self.user = []
        if room is not None:
            self.user = room.user
            self.rcode = room.rcode
        print(self.master.winfo_width()/6, self.master.winfo_width() * 4/6)
        self.rechts = tk.Frame(self, width=int(self.master.winfo_width()/6), height=int(self.master.winfo_height()),
                               bg="grey")
        self.links = tk.Frame(self, width=int(self.master.winfo_width()/6), height=int(self.master.winfo_height()),
                              bg="grey")
        self.mitte = tk.Frame(self, width=int(self.master.winfo_width() * 4/6), height=int(self.master.winfo_height()),
                              bg="white")

        self.rechts.pack_propagate(False)
        self.mitte.pack_propagate(False)
        self.links.pack_propagate(False)

        self.rechts.grid_propagate(False)
        self.mitte.grid_propagate(False)
        self.links.grid_propagate(False)

        self.rechts.grid(column=0, row=0)
        self.mitte.grid(column=1, row=0)
        self.links.grid(column=2, row=0)

        self.rc = tk.Label(self.mitte, text="Roomcode: "+self.rcode, font=("Courier", 22))
        self.l1 = tk.Label(self.rechts, text="User: ", font=("Courier", 22))

        games = ["Sudoku"]
        self.gamevar = tk.StringVar(master)
        self.gamevar.set(games[0])
        self.game = tk.OptionMenu(self.mitte, self.gamevar, *games)

        difs = ["sehr leicht", "leicht", "mittel", "schwer"]
        self.difvar = tk.StringVar(master)
        self.difvar.set(difs[0])
        self.dif = tk.OptionMenu(self.mitte, self.difvar, *difs)

        self.start = tk.Button(self.mitte, text="Start the game:", command=self.start_game, width=11,
                               font=("Courier", 20), bg="YELLOW")

        self.rc.pack()
        self.l1.pack()
        self.display_user()
        self.game.pack()
        self.dif.pack()
        self.start.pack()

    def handleresponse(self, args):
        print(args)
        base = int(args[1])
        matrix = []
        temp = args[0].split(";")
        for i in temp:
            matrix.append(list(map(lambda x: int(x), i.split(" "))))
        print(base)
        print(matrix)
        # self.pack_forget()
        # s = SudokuPage(self.master, matrix, self)
        # s.pack()
        self.master.switch_frame(SudokuPage, matrix, self)

    def start_game(self):
        serv.send_msg("setgame:" + self.gamevar.get())
        time.sleep(0.1)
        serv.send_msg("setdif:" + self.difvar.get())
        time.sleep(0.1)
        serv.send_msg("startgame")

    def display_user(self):
        for w in self.rechts.winfo_children()[1:]:
            w.destroy()
        for u in self.user:
            l = tk.Label(self.rechts, text=u, font=("Courier", 17))
            l.pack()

    def refresh_user(self, args):
        self.user = args[0].split(";")
        self.display_user()


class MainPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.t = tk.Label(self, text="", font=("Courier", 20), fg="red")
        self.join = tk.Button(self, text="Join Room:", command=self.jroom, width=11, font=("Courier", 44),
                              bg="YELLOW")
        self.cod = tk.Entry(self, width=10, font=("Courier", 44))
        self.make = tk.Button(self, text='Make new Room', command=self.mroom, width=15, font=("Courier", 44),
                              bg="YELLOW")
        relx = 0.4
        self.t.place(relx=0.5, rely=0.1, anchor="center")
        self.join.place(relx=relx, rely=0.2, anchor="e")
        self.cod.place(relx=relx + 0.01, rely=0.2, anchor="w")
        self.make.place(relx=0.5, rely=0.8, anchor="center")


    def changetxt(self, txt):
        self.t.configure(text=txt)

    def jroom(self):
        self.handleresponse_mroom(['hhdf', 'dsgf'])
        s = self.cod.get()
        print(s)
        self.make["state"] = "disabled"
        self.cod["state"] = "disabled"
        serv.send_msg("joinroom:" + s)
        # wait for accept from server then do sth

    def mroom(self):
        self.make["state"] = "disabled"
        serv.send_msg("makeroom")
        # get Roomcode then switch to Roompage

    def handleresponse_jroom(self, args):
        if args[0] == "True":
            self.master.switch_frame(RoomPage, self.cod.get())
        else:
            self.changetxt(args[1])
            self.join["state"] = "normal"

    def handleresponse_mroom(self, args):
        self.master.switch_frame(LeaderboardPage, args[0])


class RegisterPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.t = tk.Label(self, text="Passwords are not safely encrypted", font=("Courier", 20), fg="red")
        self.l1 = tk.Label(self, text="Username: ", font=("Courier", 44))
        self.l2 = tk.Label(self, text="Password: ", font=("Courier", 44))
        self.l3 = tk.Label(self, text="Repeat: ", font=("Courier", 44))
        self.usern = tk.Entry(self, width=10, font=("Courier", 44))
        self.passw = tk.Entry(self, width=10, font=("Courier", 44), show="*")
        self.rep = tk.Entry(self, width=10, font=("Courier", 44), show="*")
        self.reg = tk.Button(self, text='Register', command=self.get_entries, width=10, font=("Courier", 44),
                             bg="YELLOW")
        self.login = tk.Button(self, text='Login', command=self.switchLog, width=10, font=("Courier", 44), bg="YELLOW")

        relx = 0.4
        self.t.place(relx=0.5, rely=0.1, anchor="center")
        self.l1.place(relx=relx, rely=0.2, anchor="e")
        self.l2.place(relx=relx, rely=0.4, anchor="e")
        self.l3.place(relx=relx, rely=0.6, anchor="e")
        self.usern.place(relx=relx, rely=0.2, anchor="w")
        self.passw.place(relx=relx, rely=0.4, anchor="w")
        self.rep.place(relx=relx, rely=0.6, anchor="w")
        self.reg.place(relx=relx, rely=0.8, anchor="e")
        self.login.place(relx=relx+0.1, rely=0.8, anchor="w")
        # self.reg.place(relx=relx + 0.05 + 0.05, rely=0.7, anchor="w")
        # self.check.place(relx=0.85, rely=0.5, anchor="e")
        # self.check = tk.Button(master, text="show", command=self.show, width=5, font=("Courier", 40), bg="YELLOW")
        # self.check.place(relx=0.85, rely=0.5, anchor="center")

    def changetxt(self, txt):
        self.t.configure(text=txt)

    def switchLog(self):
        self.master.switch_frame(LoginPage)

    def get_entries(self):
        usern = self.usern.get()
        passw = self.passw.get()
        passw2 = self.rep.get()
        if not passw == passw2:
            self.changetxt("Passwords have too be the same")
            return
        elif not (usern and passw and passw2):
            self.changetxt("Missing stuff")
            return
        self.reg["state"] = "disabled"
        print(usern, passw)
        # send to Server and wait for reply
        serv.send_msg("register:" + usern + "," + passw)

    def handleresponse(self, args):
        if args[0] == "True":
            self.master.switch_frame(MainPage)
        else:
            self.changetxt(args[1])
            self.login["state"] = "normal"


class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.t = tk.Label(self, text="", font=("Courier", 20), fg="red")
        self.l1 = tk.Label(self, text="Username: ")
        self.l2 = tk.Label(self, text="Password: ")
        self.l1.config(font=("Courier", 44))
        self.l2.config(font=("Courier", 44))
        self.usern = tk.Entry(self, width=10, font=("Courier", 44))
        self.passw = tk.Entry(self, width=10, font=("Courier", 44), show="*")
        self.login = tk.Button(self, text='Login', command=self.get_entries, width=10, font=("Courier", 44),
                               bg="YELLOW")
        self.reg = tk.Button(self, text='Register', command=self.switch_to_reg,
                             width=10, font=("Courier", 44), bg="YELLOW")
        self.check = tk.Button(self, text="show", command=self.show, width=5, font=("Courier", 40), bg="YELLOW")

        relx = 0.4
        self.t.place(relx=0.5, rely=0.1, anchor="center")
        self.l1.place(relx=relx, rely=0.3, anchor="e")
        self.l2.place(relx=relx, rely=0.5, anchor="e")
        self.usern.place(relx=relx, rely=0.3, anchor="w")
        self.passw.place(relx=relx, rely=0.5, anchor="w")
        self.login.place(relx=relx, rely=0.7, anchor="e")
        self.reg.place(relx=relx+0.05+0.05, rely=0.7, anchor="w")
        self.check.place(relx=0.85, rely=0.5, anchor="e")
        # self.b2 = tk.Button(master, text='Register', command=dosth).grid(row=3, column=1, sticky=W, pady=4)

    def changetxt(self, txt):
        self.t.configure(text=txt)

    def switch_to_reg(self):
        self.master.switch_frame(RegisterPage)

    def show(self):
        self.passw.configure(show="")
        self.check.configure(text="hide", command=self.hide)

    def hide(self):
        self.passw.configure(show="*")
        self.check.configure(text="show", command=self.show)

    def get_entries(self):
        usern = self.usern.get()
        passw = self.passw.get()
        if not (usern and passw):
            self.changetxt("Missing stuff")
            return
        self.login["state"] = "disabled"
        print(usern, passw)
        serv.send_msg("login:" + usern + "," + passw)
        # send to Server and wait for reply

    def handleresponse(self, args):    # b = boolean
        print(args)
        if args[0] == "True":
            self.master.switch_frame(MainPage)
        else:
            self.changetxt(args[1])
            self.login["state"] = "normal"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.fr = None
        print(self.fr)
        self.w = 1280
        self.h = int(self.w * 13 / 21)
        self.geometry(str(self.w) + "x" + str(self.h))

    def switch_frame(self, frame_class, *args):
        new_frame = frame_class(self, *args)
        if self.fr is not None:
            self.fr.destroy()
        self.fr = new_frame
        self.fr.pack(fill="both", expand="yes")
        print(self.fr)
        # self.fr.pack()

    def start(self):
        self.fr = SudokuPage(self, smatrix, 10000)
        self.fr.pack(fill="both", expand="yes")
        print(self.fr)
        self.mainloop()

a = App()
a.start()
