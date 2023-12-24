from datetime import datetime
import os
import time

LETTER = ["", "a", "b", "c", "d", "e", "f", "g", "h"]


def encode(fro, to, promote=None):
    data = LETTER[fro[0]] + str(9 - fro[1]) + LETTER[to[0]] + str(9 - to[1])
    if promote is not None:
        return data + promote
    return data


def decode(data):
    ret = [
        [LETTER.index(data[0]), 9 - int(data[1])],
        [LETTER.index(data[2]), 9 - int(data[3])],
    ]
    if len(data) == 5:
        ret.append(data[4])
    else:
        ret.append(None)
    return ret


def initBoardVars():
    side = False
    board = [
        [
            [1, 7, "p"], [2, 7, "p"], [3, 7, "p"], [4, 7, "p"],
            [5, 7, "p"], [6, 7, "p"], [7, 7, "p"], [8, 7, "p"],
            [1, 8, "r"], [2, 8, "n"], [3, 8, "b"], [4, 8, "q"],
            [5, 8, "k"], [6, 8, "b"], [7, 8, "n"], [8, 8, "r"],
        ], [
            [1, 2, "p"], [2, 2, "p"], [3, 2, "p"], [4, 2, "p"],
            [5, 2, "p"], [6, 2, "p"], [7, 2, "p"], [8, 2, "p"],
            [1, 1, "r"], [2, 1, "n"], [3, 1, "b"], [4, 1, "q"],
            [5, 1, "k"], [6, 1, "b"], [7, 1, "n"], [8, 1, "r"],
        ]
    ]
    flags = [[True for _ in range(4)], None]
    return side, board, flags


def undo(moves, num=1):
    if len(moves) in range(num):
        return moves
    else:
        return moves[:-num]


def getSFpath():
    conffile = os.path.join("res", "stockfish", "path.txt")
    if os.path.exists(conffile):
        with open(conffile, "r") as f:
            return f.read().strip()


def rmSFpath():
    os.remove(os.path.join("res", "stockfish", "path.txt"))


def getTime():
    return round(time.perf_counter() * 1000)


def updateTimer(side, mode, timer):
    if timer is None:
        return None

    ret = list(timer)
    if mode != -1:
        ret[side] += (mode * 1000)
    return ret


def saveGame(moves, gametype="multi", player=0, level=0,
             mode=None, timer=None, cnt=0):
    if cnt >= 20:
        return -1

    name = os.path.join("res", "savedGames", "game" + str(cnt) + ".txt")
    if os.path.isfile(name):
        return saveGame(moves, gametype, player, level, mode, timer, cnt + 1)

    else:
        if gametype == "single":
            gametype += " " + str(player) + " " + str(level)
        if gametype == "mysingle":
            gametype += " " + str(player)

        dt = datetime.now()
        date = "/".join(map(str, [dt.day, dt.month, dt.year]))
        time = ":".join(map(str, [dt.hour, dt.minute, dt.second]))
        datentime = " ".join([date, time])

        movestr = " ".join(moves)

        temp = []
        if mode is not None:
            temp.append(str(mode))

            if timer is not None:
                temp.extend(map(str, timer))

        temp = " ".join(temp)
        text = "\n".join([gametype, datentime, movestr, temp])

        with open(name, "w") as file:
            file.write(text)
        return cnt
