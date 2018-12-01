import os
import sys
import random as r
import pygame as pg
from pygame import *
import time

screenx = 650
screeny = 650
screenName = "The Snake Game"

bgCol = (50, 255, 102)
black = (0, 0, 0)
white = (255, 255, 255) 
red = (255, 0 ,0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

pg.init()
screen = pg.display.set_mode((screenx, screeny))
pg.display.set_caption(screenName)

bgm = pg.mixer.Sound('./nyan.wav')
eft = pg.mixer.Sound('./video.wav')
death = pg.mixer.Sound('./death.wav')
fontObj = pg.font.Font('./geforce-bold.ttf', 30)
score = 0
pg.mixer.Sound.play(bgm)

clock = pg.time.Clock()
fps = 8

gamePlate = []
snakePos = [(3,1), (2,1), (1,1)]
applePos = [0, 0]
appleCK = False
gamestatus = True

horizontalSize = 25
verticalSize = 25
marginSize = 1
horizontaldir = 1
verticaldir = 0
horizontalRow = []

def applePosSet():
    global appleCK
    global applePos
    bV = 0
    if appleCK == False:
        while True:
            bV = 0
            x = r.randint(1, horizontalSize - 2)
            y = r.randint(1, verticalSize - 2)
            
            for n in range(snakeLength):
                if x == snakePos[n][0] and y == snakePos[n][1]:
                    bV = 1
                    
            if bV == 0:
                break

        applePos = [x, y]
        gamePlate[applePos[1]][applePos[0]] = 7
        appleCK = True

        

for x in range(0, horizontalSize):
    for y in range(0, verticalSize):
        if x == 0 or x == horizontalSize - 1 or y == 0 or y == verticalSize - 1:
            horizontalRow.append(5)
        else:
            horizontalRow.append(0)

    gamePlate.append(horizontalRow)
    horizontalRow = []


def score_to_screen():
    scoreSurf = fontObj.render(str(score), True, red, bgCol)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (50, 50)
    screen.blit(scoreSurf, scoreRect)

def plateDisplay():
    for n in gamePlate:
        print(n)
    print()

        
def snakePosCal():
    global appleCK
    global applePos
    global gamestatus
    global score

    posx = snakePos[0][0]  
    posy = snakePos[0][1]

    posx += horizontaldir
    posy += verticaldir

    if posx < 1 or posy < 1 or posx > horizontalSize - 2 or posy > verticalSize - 2:
        gamestatus = False
    
    snakePos.insert(0, (posx, posy))
    snakePos.pop(-1)

    for x in range(horizontalSize):
        for y in range(verticalSize):
            for n in range(snakeLength):
                if x == snakePos[n][0] and y == snakePos[n][1]:
                    gamePlate[y][x] = 8

    if snakePos[0][0] == applePos[0] and snakePos[0][1] == applePos[1]:
        tailx = snakePos[-1][0]
        taily = snakePos[-1][1]
        snakePos.insert(-1, (tailx, taily))
        appleCK = False
        score += 1
        pg.mixer.Sound.stop(bgm)
        pg.mixer.Sound.play(eft)
        pg.mixer.Sound.play(bgm)

    for n in range(snakeLength):
        
        if snakePos[0][0] == snakePos[n][0] and snakePos[0][1] == snakePos[n][1] and n != 0:
            gamestatus = False
            

def snakePosDisplay():
    for n in range(snakeLength):
        print(snakePos[n])
    print()

def gamePlateBorderDrawing():

    for x in range(0, horizontalSize):
        startPoint = (screenx / horizontalSize * x, 0)
        endPoint = (screenx / horizontalSize * x, screeny)

        pg.draw.line(screen, black, startPoint, endPoint, marginSize)
        pg.draw.line(screen, black, (screenx, 0), (screenx, screeny))

    for y in range(0, verticalSize):
        startPoint = (0, screeny / verticalSize * y)
        endPoint = (screenx, screeny / verticalSize * y)

        pg.draw.line(screen, black, startPoint, endPoint, marginSize)
        pg.draw.line(screen, black, (0, screeny), (screenx, screeny))

def screenUpdate():
    a = True
    screen.fill(bgCol)
    for x in range(horizontalSize):
        for y in range(verticalSize):
            if y != verticalSize -1 and y != 0 and x != horizontalSize -1 and x != 0:
                if x == applePos[0] and y == applePos[1]:
                    pass
                else:
                    gamePlate[y][x] = 0

        

    snakePosCal()
    applePosSet()
    


    for n in range(len(gamePlate)):                     #wall coloring
        for m in range(len(gamePlate[n])):
            if gamePlate[n][m] == 5:
                pg.draw.rect(screen, blue, (m * screenx / horizontalSize, n * screeny / verticalSize, screenx / horizontalSize, screeny / verticalSize), 0)
            if gamePlate[n][m] == 7:
                pg.draw.rect(screen, yellow, (m * screenx / horizontalSize, n * screeny / verticalSize, screenx / horizontalSize, screeny / verticalSize), 0)
            if gamePlate[n][m] == 8:
                pg.draw.rect(screen, red, (m * screenx / horizontalSize, n * screeny / verticalSize, screenx / horizontalSize, screeny / verticalSize), 0)

    
    gamePlateBorderDrawing()

screen.fill(bgCol)
start = fontObj.render('Welcome To The World Of Snakes', True, blue, bgCol)
SR = start.get_rect()
SR.topleft = (screenx / 5 , screeny / 5)
screen.blit(start, SR)
pg.display.update()
time.sleep(5)

while True:
    if gamestatus == False:
        pg.mixer.Sound.stop(bgm)
        pg.mixer.Sound.stop(eft)
        pg.mixer.Sound.play(death)
        time.sleep(5)
        pg.quit()
        sys.exit()

    
    fpsCount = 0
    snakeLength = len(snakePos)

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            keyPressed = event.key
            print(keyPressed , " Pressed")

            if keyPressed == K_ESCAPE:
                gamestatus = False
            
    if snakePos[0][0] < applePos[0]:
        #if horizontaldir != -1:
            horizontaldir = 1
            verticaldir = 0
    
    elif snakePos[0][1] < applePos[1]:
        #if verticaldir != -1:
            verticaldir = 1
            horizontaldir = 0

    if snakePos[0][0] > applePos[0]:
        #if horizontaldir != 1:
            horizontaldir = -1
            verticaldir = 0
  
    elif snakePos[0][1] > applePos[1]:
        #if verticaldir != 1:
            verticaldir = -1
            horizontaldir = 0
    
    screenUpdate()
    score_to_screen()
    plateDisplay()
    snakePosDisplay()
    print(snakeLength)
    print("--------------------------------------------------")
    pg.display.update()
    fpsCount += 1
    clock.tick(fps)