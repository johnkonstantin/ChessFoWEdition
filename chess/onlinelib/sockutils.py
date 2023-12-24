import queue
import socket

q = queue.Queue()
isdead = True


def bgThread(sock):
    global isdead
    isdead = False
    while True:
        try:
            msg = sock.recv(8).decode("utf-8").strip()

        except:
            break

        if not msg or msg == "close":
            break

        if msg != "........":
            q.put(msg)
    isdead = True


def isDead():
    return q.empty() and isdead


def read():
    if isDead():
        return "close"
    return q.get()


def readable():
    if isDead():
        return True
    return not q.empty()


def flush():
    while readable():
        if read() == "close":
            return False
    return True


def write(sock, msg):
    if msg:
        buffedmsg = msg + (" " * (8 - len(msg)))
        try:
            sock.sendall(buffedmsg.encode("utf-8"))
        except:
            pass


def getPlayers(sock):
    if not flush():
        return None

    write(sock, "pStat")

    msg = read()
    if msg.startswith("enum"):
        data = []
        for i in range(int(msg[-1])):
            newmsg = read()
            if newmsg == "close":
                return None
            else:
                data.append(newmsg)
        return tuple(data)
