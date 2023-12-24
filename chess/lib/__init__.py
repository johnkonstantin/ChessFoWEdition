fags = [[True for _ in range(4)], None]

from chess.lib.core import (
    getType,
    isOccupied,
    isChecked,  
    isEnd,
    isValidMove,
    availableMoves,
    makeMove, 
)
from chess.lib.gui import (
    pygame,
    CHESS,
    BACK,
    sound,
    getChoice,
    showTimeOver,
    putClock,
    drawBoard,
    drawPieces,
    prompt,
    start, 
)
from chess.lib.utils import (
    encode,
    decode,
    initBoardVars,
    undo,
    getSFpath,
    rmSFpath,
    getTime,
    updateTimer,
    saveGame,
)
from chess.lib.ai import miniMax

def convertMoves(moves):
    side, board, flags = initBoardVars()

    for fro, to, promote in map(decode, moves):
        side, board, flags = makeMove(side, board, fro, to, flags, promote)

    return side, board, flags

def getPromote(win, side, board, fro, to, single=False):
    if getType(side, board, fro) == "p":
        if (side == 0 and to[1] == 1) or (side == 1 and to[1] == 8):
            if single:
                return "q"
            else:
                return getChoice(win, side)

def showClock(win, side, mode, timer, start, timedelta):
    if timer is None:
        pygame.display.update()
        return None
    
    ret = list(timer)
    elaptime = getTime() - (start + timedelta)
    if mode == -1:
        ret[side] += elaptime
        if ret[side] >= 3600000:
            ret[side] = 3599000
            
    else:
        ret[side] -= elaptime
        if ret[side] < 0:
            showTimeOver(win, side)
            return None
    
    putClock(win, ret)
    return ret

def showAvailMoves(win, side, board, pos, flags, flip):
    piece = pos + [getType(side, board, pos)]
    for i in availableMoves(side, board, piece, flags):
        x = 470 - i[0] * 50 if flip else i[0] * 50 + 20
        y = 470 - i[1] * 50 if flip else i[1] * 50 + 20
        pygame.draw.rect(win, (0, 255, 0), (x, y, 10, 10))

def animate(win, side, board, fro, to, load, player=None):
    if side == player:
        sound.play_drag(load)
        if player is None:
            FLIP = side and load["flip"]
        else:
            FLIP = player and load["flip"]

        piece = CHESS.PIECES[side][getType(side, board, fro)]
        x1, y1 = fro[0] * 50, fro[1] * 50
        x2, y2 = to[0] * 50, to[1] * 50
        if FLIP:
            x1, y1 = 450 - x1, 450 - y1
            x2, y2 = 450 - x2, 450 - y2

        stepx = (x2 - x1) / 50
        stepy = (y2 - y1) / 50

        col = (180, 100, 30) if (fro[0] + fro[1]) % 2 else (220, 240, 240)

        clk = pygame.time.Clock()
        for i in range(51):
            clk.tick_busy_loop(100)
            drawBoard(win)
            drawPieces(win, board, FLIP, player, fags)

            pygame.draw.rect(win, col, (x1, y1, 50, 50))
            win.blit(piece, (x1 + (i * stepx), y1 + (i * stepy)))
            pygame.display.update()
        sound.play_move(load)

def showScreen(win, side, board, flags, pos, load, player=None, online=False):
    fags = flags
    multi = False
    if player is None:
        multi = True
        player = side

    flip = load["flip"] and player

    drawBoard(win)
    win.blit(BACK, (460, 0))
    
    if not multi:
        win.blit(CHESS.TURN[int(side == player)], (10, 460))
        
    if not online:
        if load["allow_undo"]:
            win.blit(CHESS.UNDO, (10, 12))
        win.blit(CHESS.SAVE, (350, 462))

    if isEnd(side, board, flags):
        if isChecked(side, board):
            win.blit(CHESS.CHECKMATE, (100, 12))
            win.blit(CHESS.LOST, (320, 12))
            win.blit(CHESS.PIECES[side]["k"], (270, 0))
        else:
            win.blit(CHESS.STALEMATE, (160, 12))
    else:
        if online:
            win.blit(CHESS.DRAW, (10, 12))
            win.blit(CHESS.RESIGN, (400, 462))
            
        if isChecked(side, board):
            win.blit(CHESS.CHECK, (200, 12))

        if isOccupied(side, board, pos) and side == player:
            x = (9 - pos[0]) * 50 if flip else pos[0] * 50
            y = (9 - pos[1]) * 50 if flip else pos[1] * 50
            pygame.draw.rect(win, (255, 255, 0), (x, y, 50, 50))

    drawPieces(win, board, flip, player, fags)
    if load["show_moves"] and side == player:
        showAvailMoves(win, side, board, pos, flags, flip)
        
    if not multi:
        pygame.display.update()
