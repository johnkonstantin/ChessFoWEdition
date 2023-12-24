import sys
import pygame

import chess
import menus
from tools.loader import MAIN
from tools import sound

sys.stdout.flush()

pygame.init()
clock = pygame.time.Clock()

if pygame.version.vernum[0] >= 2:
    win = pygame.display.set_mode((500, 500), pygame.SCALED)
else:
    win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Chess: FogOfWar Edition")
pygame.display.set_icon(MAIN.ICON)

onln = (160, 400, 120, 40)


def showMain(prefs):
    global cnt, img

    win.blit(MAIN.BG[img], (0, 0))
    cnt = -150
    img = 0

    win.blit(MAIN.HEADING, (80, 20))
    win.blit(MAIN.VERSION, (345, 55))

    win.blit(MAIN.ONLINE, onln[:2])


cnt = 0
img = 0
run = True

prefs = {'sounds': False, 'flip': False, 'slideshow': True, 'show_moves': True, 'allow_undo': True, 'show_clock': False}

music = sound.Music()
music.play(prefs)
while run:
    clock.tick(30)
    showMain(prefs)

    x, y = pygame.mouse.get_pos()

    if onln[0] < x < sum(onln[::2]) and onln[1] < y < sum(onln[1::2]):
        win.blit(MAIN.ONLINE_H, onln[:2])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if onln[0] < x < sum(onln[::2]) and onln[1] < y < sum(onln[1::2]):
                sound.play_click(prefs)
                ret = menus.onlinemenu(win)
                if ret == 0:
                    run = False
                elif ret != 1:
                    run = chess.online(win, ret[0], prefs)

    pygame.display.flip()

music.stop()
pygame.quit()
