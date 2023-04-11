from Server import Server
serv = Server('192.168.178.117', 12345)

rcode = "54321"

responses = {
    "login": None,
    "register": None,
    "makeroom": None,
    "joinroom": None,
}
import GUI
a = GUI.App()