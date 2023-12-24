import os.path
import pygame

pygame.font.init()
FONT = os.path.join("res", "Asimov.otf")

head = pygame.font.Font(FONT, 80)
large = pygame.font.Font(FONT, 50)
medium = pygame.font.Font(FONT, 38)
small = pygame.font.Font(FONT, 27)
vsmall = pygame.font.Font(FONT, 17)

WHITE = (255, 255, 255)
GREY = (180, 180, 180)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (200, 20, 20)

NUM = [vsmall.render(str(i), True, WHITE) for i in range(10)]
LNUM = [small.render(str(i), True, WHITE) for i in range(10)]
BLNUM = [small.render(str(i), True, BLACK) for i in range(10)]
SLASH = vsmall.render("/", True, WHITE)
COLON = vsmall.render(":", True, WHITE)


def putNum(win, num, pos):
    for cnt, i in enumerate(list(str(num))):
        win.blit(NUM[int(i)], (pos[0] + (cnt * 9), pos[1]))


def putLargeNum(win, num, pos, white=True):
    for cnt, i in enumerate(list(str(num))):
        if white:
            win.blit(LNUM[int(i)], (pos[0] + (cnt * 14), pos[1]))
        else:
            win.blit(BLNUM[int(i)], (pos[0] + (cnt * 14), pos[1]))


def putDT(win, DT, pos):
    var = DT.split()
    date = var[0].split("/")
    time = var[1].split(":")

    for cnt, num in enumerate(map(lambda x: format(int(x), "02"), date)):
        putNum(win, num, (pos[0] + 24 * cnt - 5, pos[1]))

    win.blit(SLASH, (pos[0] + 13, pos[1]))
    win.blit(SLASH, (pos[0] + 35, pos[1]))

    for cnt, num in enumerate(map(lambda x: format(int(x), "02"), time)):
        putNum(win, num, (pos[0] + 24 * cnt, pos[1] + 21))

    win.blit(COLON, (pos[0] + 20, pos[1] + 21))
    win.blit(COLON, (pos[0] + 44, pos[1] + 21))


def splitstr(string, index=57):
    data = []
    while len(string) >= index:
        data.append(string[:index])
        string = string[index:]
    data.append(string)
    return data


BGSPRITE = pygame.image.load(os.path.join("res", "img", "bgsprites.jpg"))
PSPRITE = pygame.image.load(os.path.join("res", "img", "piecesprite.png"))

BACK = pygame.image.load(os.path.join("res", "img", "back.png"))


class CHESS:
    PIECES = ({}, {})
    for i, ptype in enumerate(["k", "q", "b", "n", "r", "p"]):
        for side in range(2):
            PIECES[side][ptype] = PSPRITE.subsurface((i * 50, side * 50, 50, 50))

    CHECK = small.render("CHECK!", True, BLACK)
    STALEMATE = small.render("STALEMATE!", True, BLACK)
    CHECKMATE = small.render("CHECKMATE!", True, BLACK)
    LOST = small.render("LOST", True, BLACK)
    CHOOSE = small.render("CHOOSE:", True, BLACK)
    SAVE = small.render("Save Game", True, BLACK)
    UNDO = small.render("Undo", True, BLACK)

    MESSAGE = (
        small.render("Do you want to quit", True, WHITE),
        small.render("this game?", True, WHITE),
    )

    MESSAGE2 = (
        small.render("Game saved. Now do", True, WHITE),
        small.render("you want to quit?", True, WHITE),
    )

    YES = small.render("YES", True, WHITE)
    NO = small.render("NO", True, WHITE)
    MSG = vsmall.render("Game will be saved with ID", True, WHITE)
    SAVE_ERR = vsmall.render("ERROR: SaveGame Limit Exeeded", True, WHITE)

    TURN = (
        small.render("Others turn", True, BLACK),
        small.render("Your turn", True, BLACK),
    )

    DRAW = small.render("Draw", True, BLACK)
    RESIGN = small.render("Resign", True, BLACK)

    TIMEUP = (
        vsmall.render("Time Up!", True, WHITE),
        vsmall.render("Technically the game is over, but you", True, WHITE),
        vsmall.render("can still continue if you wish to - :)", True, WHITE),
    )

    OK = small.render("Ok", True, WHITE)
    COL = small.render(":", True, BLACK)


class LOADGAME:
    HEAD = large.render("Load Games", True, WHITE)
    LIST = medium.render("List of Games", True, WHITE)
    EMPTY = small.render("There are no saved games yet.....", True, WHITE)
    GAME = small.render("Game", True, WHITE)
    TYPHEAD = vsmall.render("Game Type:", True, WHITE)
    TYP = {
        "multi": vsmall.render("MultiPlayer", True, WHITE),
    }
    DATE = vsmall.render("Date-", True, WHITE)
    TIME = vsmall.render("Time-", True, WHITE)

    DEL = pygame.image.load(os.path.join("res", "img", "delete.jpg"))
    LOAD = small.render("LOAD", True, WHITE)

    MESSAGE = (
        small.render("Are you sure that you", True, WHITE),
        small.render("want to delete game?", True, WHITE),
    )
    YES = small.render("YES", True, WHITE)
    NO = small.render("NO", True, WHITE)

    LEFT = medium.render("<", True, WHITE)
    RIGHT = medium.render(">", True, WHITE)
    PAGE = [medium.render("Page " + str(i), True, WHITE) for i in range(1, 5)]


class MAIN:
    HEADING = small.render("Chess: FogOfWar Edition", True, WHITE)
    VERSION = vsmall.render("Version 1.1", True, WHITE)
    ICON = pygame.image.load(os.path.join("res", "img", "icon.gif"))
    BG = [BGSPRITE.subsurface((i * 500, 0, 500, 500)) for i in range(4)]

    SINGLE = medium.render("SinglePlayer", True, WHITE)
    MULTI = medium.render("MultiPlayer", True, WHITE)
    ONLINE = medium.render("Start game", True, WHITE)
    LOAD = medium.render("Load Game", True, WHITE)
    HOWTO = small.render("Howto", True, WHITE)
    ABOUT = medium.render("About", True, WHITE)
    PREF = medium.render("Preferences", True, WHITE)
    STOCK = small.render("Configure Stockfish", True, WHITE)

    SINGLE_H = medium.render("SinglePlayer", True, GREY)
    MULTI_H = medium.render("MultiPlayer", True, GREY)
    ONLINE_H = medium.render("Start game", True, GREY)
    LOAD_H = medium.render("Load Game", True, GREY)
    HOWTO_H = small.render("Howto", True, GREY)
    ABOUT_H = medium.render("About", True, GREY)
    PREF_H = medium.render("Preferences", True, GREY)
    STOCK_H = small.render("Configure Stockfish", True, GREY)

class ONLINE:
    ERR = (
        vsmall.render("Attempting to connect to server..", True, WHITE),
        vsmall.render("[ERR 1] Couldn't find the server..", True, WHITE),
        vsmall.render("[ERR 2] Versions are incompatible..", True, WHITE),
        vsmall.render("[ERR 3] Server is full (max = 10)..", True, WHITE),
        vsmall.render("[ERR 4] The server is locked...", True, WHITE),
        vsmall.render("[ERR 5] Unknown error occured...", True, WHITE),
        vsmall.render("You got disconnected from server..", True, WHITE),
    )
    GOBACK = vsmall.render("Go Back", True, WHITE)

    EMPTY = small.render("No one's online, you are alone.", True, WHITE)

    LOBBY = large.render("Online Lobby", True, WHITE)
    LIST = medium.render("List of Players", True, WHITE)
    PLAYER = small.render("Player", True, WHITE)
    DOT = small.render(".", True, WHITE)

    ACTIVE = small.render("ACTIVE", True, GREEN)
    BUSY = small.render("BUSY", True, RED)
    REQ = small.render("Send Request", True, WHITE)
    YOUARE = medium.render("You Are", True, WHITE)

    ERRCONN = vsmall.render("Unable to connect to that player..", True, WHITE)

    REFRESH = pygame.image.load(os.path.join("res", "img", "refresh.png"))

    REQUEST1 = (
        vsmall.render("Please wait for the other player to", True, WHITE),
        vsmall.render("accept your request. Game will begin", True, WHITE),
        vsmall.render("shortly. You will play as white", True, WHITE),
    )
    REQUEST2 = (
        vsmall.render("Player", True, WHITE),
        vsmall.render("wants to play with you.", True, WHITE),
        vsmall.render("Accept to play. You will play as black", True, WHITE),
    )

    DRAW1 = (
        vsmall.render("Sent a request to your opponent for", True, WHITE),
        vsmall.render("draw, wait for reply.", True, WHITE),
    )

    DRAW2 = (
        vsmall.render("Your opponent is requesting for a", True, WHITE),
        vsmall.render("draw, please reply.", True, WHITE),
    )

    POPUP = {
        "quit": vsmall.render("Opponent got disconnected", True, WHITE),
        "resign": vsmall.render("The opponent has resigned", True, WHITE),
        "draw": vsmall.render("A draw has been agreed", True, WHITE),
        "end": vsmall.render("Game ended, opponent left", True, WHITE),
        "abandon": vsmall.render("Opponent abandoned match", True, WHITE),
    }

    NO = small.render("NO", True, WHITE)
    OK = small.render("OK", True, WHITE)


class ONLINEMENU:
    HEAD = large.render("Online", True, WHITE)
    with open(os.path.join("res", "texts", "online.txt")) as f:
        TEXT = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]

    CONNECT = small.render("Connect", True, WHITE)


pygame.font.quit()
