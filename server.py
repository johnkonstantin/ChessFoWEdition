import queue
import random
import socket
import threading
import time
from urllib.request import urlopen

LOG = False

VERSION = "v3.2.0"
PORT = 26104
START_TIME = time.perf_counter()
LOGFILENAME = time.asctime().replace(" ", "_").replace(":", "-")

busyPpl = set()
end = False
lock = False
logQ = queue.Queue()
players = []
total = totalsuccess = 0


def makeInt(num):
    try:
        return int(num)
    except ValueError:
        return None


def getTime():
    sec = round(time.perf_counter() - START_TIME)
    minutes, sec = divmod(sec, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days} days, {hours} hours, {minutes} minutes, {sec} seconds"


def getIp(public):
    if public:
        try:
            ip = urlopen("https://api64.ipify.org").read().decode()
        except:
            ip = "127.0.0.1"

    else:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                s.connect(('10.255.255.255', 1))
                ip = s.getsockname()[0]
            except:
                ip = '127.0.0.1'
    return ip


def log(data, key=None, adminput=False):
    global logQ
    if adminput:
        text = ""
    elif key is None:
        text = "SERVER: "
    else:
        text = f"Player{key}: "

    if data is not None:
        text += data
        if not adminput:
            print(text)

        if LOG:
            logQ.put(time.asctime() + ": " + text + "\n")
    else:
        logQ.put(None)


def read(sock, timeout=None):
    try:
        sock.settimeout(timeout)
        msg = sock.recv(8).decode("utf-8").strip()

    except:
        msg = "quit"

    if msg:
        return msg
    return "quit"


def write(sock, msg):
    if msg:
        buffedmsg = msg + (" " * (8 - len(msg)))
        try:
            sock.sendall(buffedmsg.encode("utf-8"))
        except:
            pass


def genKey():
    key = random.randint(1000, 9999)
    for player in players:
        if player[1] == key:
            return genKey()
    return key


def getByKey(key):
    for player in players:
        if player[1] == makeInt(key):
            return player[0]


def mkBusy(*keys):
    global busyPpl
    for key in keys:
        busyPpl.add(makeInt(key))


def rmBusy(*keys):
    global busyPpl
    for key in keys:
        busyPpl.discard(makeInt(key))


def game(sock1, sock2):
    while True:
        msg = read(sock1)
        write(sock2, msg)
        if msg == "quit":
            return True

        elif msg in ["draw", "resign", "end"]:
            return False


def player(sock, key):
    while True:
        msg = read(sock)
        if msg == "quit":
            return

        elif msg == "pStat":
            log("Made request for players Stats.", key)
            latestplayers = list(players)
            latestbusy = list(busyPpl)

            if 0 < len(latestplayers) < 11:
                write(sock, "enum" + str(len(latestplayers) - 1))
                for _, i in latestplayers:
                    if i != key:
                        if i in latestbusy:
                            write(sock, str(i) + "b")
                        else:
                            write(sock, str(i) + "a")

        elif msg.startswith("rg"):
            log(f"Made request to play with Player{msg[2:]}", key)
            oSock = getByKey(msg[2:])
            if oSock is not None:
                if makeInt(msg[2:]) not in busyPpl:
                    mkBusy(key, msg[2:])
                    write(oSock, "gr" + str(key))

                    write(sock, "msgOk")
                    newMsg = read(sock)
                    if newMsg == "ready":
                        log(f"Player{key} is in a game as white")
                        if game(sock, oSock):
                            return
                        else:
                            log(f"Player{key} finished the game")

                    elif newMsg == "quit":
                        write(oSock, "quit")
                        return

                    rmBusy(key)

                else:
                    log(f"Player{key} requested busy player")
                    write(sock, "errPBusy")
            else:
                log(f"Player{key} Sent invalid key")
                write(sock, "errKey")

        elif msg.startswith("gmOk"):
            log(f"Accepted Player{msg[4:]} request", key)
            oSock = getByKey(msg[4:])
            write(oSock, "start")
            log(f"Player{key} is in a game as black")
            if game(sock, oSock):
                return
            else:
                log(f"Player{key} finished the game")
                rmBusy(key)

        elif msg.startswith("gmNo"):
            log(f"Rejected Player{msg[4:]} request", key)
            write(getByKey(msg[4:]), "nostart")
            rmBusy(key)


def logThread():
    global logQ
    while True:
        time.sleep(1)
        with open("SERVER_LOG_" + LOGFILENAME + ".txt", "a") as f:
            while not logQ.empty():
                data = logQ.get()
                if data is None:
                    return
                else:
                    f.write(data)


def kickDisconnectedThread():
    global players
    while True:
        time.sleep(10)
        for sock, key in players:
            try:
                ret = sock.send(b"........")
            except:
                ret = 0

            if ret > 0:
                cntr = 0
                diff = 8
                while True:
                    cntr += 1
                    if cntr == 8:
                        ret = 0
                        break

                    if ret == diff:
                        break
                    diff -= ret

                    try:
                        ret = sock.send(b"." * diff)
                    except:
                        ret = 0
                        break

            if ret == 0:
                log(f"Player{key} got disconnected, removing from player list")
                try:
                    players.remove((sock, key))
                except:
                    pass


def adminThread():
    global end, lock
    while True:
        msg = input().strip()
        log(msg, adminput=True)

        if msg == "report":
            log(f"{len(players)} players are online right now,")
            log(f"{len(players) - len(busyPpl)} are active.")
            log(f"{total} connections attempted, {totalsuccess} were successful")
            log(f"Server is running {threading.active_count()} threads.")
            log(f"Time elapsed since last reboot: {getTime()}")
            if players:
                log("LIST OF PLAYERS:")
                for cnt, (_, player) in enumerate(players):
                    if player not in busyPpl:
                        log(f" {cnt + 1}. Player{player}, Status: Active")
                    else:
                        log(f" {cnt + 1}. Player{player}, Status: Busy")

        elif msg == "mypublicip":
            log("Determining public IP, please wait....")
            PUBIP = getIp(public=True)
            if PUBIP == "127.0.0.1":
                log("An error occurred while determining IP")

            else:
                log(f"This machine has a public IP address {PUBIP}")

        elif msg == "lock":
            if lock:
                log("Aldready in locked state")
            else:
                lock = True
                log("Locked server, no one can join now.")

        elif msg == "unlock":
            if lock:
                lock = False
                log("Unlocked server, all can join now.")
            else:
                log("Aldready in unlocked state.")

        elif msg.startswith("kick "):
            for k in msg[5:].split():
                sock = getByKey(k)
                if sock is not None:
                    write(sock, "close")
                    log(f"Kicking player{k}")
                else:
                    log(f"Player{k} does not exist")

        elif msg == "kickall":
            log("Attempting to kick everyone.")
            latestplayers = list(players)
            for sock, _ in latestplayers:
                write(sock, "close")

        elif msg == "quit":
            lock = True
            log("Attempting to kick everyone.")
            latestplayers = list(players)
            for sock, _ in latestplayers:
                write(sock, "close")

            log("Exiting application - Bye")
            log(None)

            end = True
            if IPV6:
                with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
                    s.connect(("::1", PORT, 0, 0))
            else:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(("127.0.0.1", PORT))
            return

        else:
            log(f"Invalid command entered ('{msg}').")


def initPlayerThread(sock):
    global players, total, totalsuccess
    log("New client is attempting to connect.")
    total += 1

    if read(sock, 3) != "PyChess":
        log("Client sent invalid header, closing connection.")
        write(sock, "errVer")

    elif read(sock, 3) != VERSION:
        log("Client sent invalid version info, closing connection.")
        write(sock, "errVer")

    elif len(players) >= 10:
        log("Server is busy, closing new connections.")
        write(sock, "errBusy")

    elif lock:
        log("SERVER: Server is locked, closing connection.")
        write(sock, "errLock")

    else:
        totalsuccess += 1
        key = genKey()
        log(f"Connection Successful, assigned key - {key}")
        players.append((sock, key))

        write(sock, "key" + str(key))
        player(sock, key)
        write(sock, "close")
        log(f"Player{key} has Quit")

        try:
            players.remove((sock, key))
        except:
            pass
        rmBusy(key)
    sock.close()


log(f"Welcome to My-Pychess Server, {VERSION}\n")
log("INITIALIZING...")

log("Starting server with IPv4 (default) configuration.")
mainSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mainSock.bind(("0.0.0.0", PORT))

IP = getIp(public=False)
if IP == "127.0.0.1":
    log("This machine does not appear to be connected to a network.")
    log("With this limitation, you can only serve the clients ")
    log("who are on THIS machine. Use IP address 127.0.0.1\n")

else:
    log(f"This machine has a local IP address - {IP}")

mainSock.listen(16)
log("Successfully Started.")
log(f"Accepting connections on port {PORT}\n")

threading.Thread(target=adminThread).start()
threading.Thread(target=kickDisconnectedThread, daemon=True).start()
if LOG:
    log("Logging is enabled. Starting to log all output")
    threading.Thread(target=logThread).start()

while True:
    s, _ = mainSock.accept()
    if end:
        break

    threading.Thread(target=initPlayerThread, args=(s,), daemon=True).start()
mainSock.close()
