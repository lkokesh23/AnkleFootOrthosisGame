# dibuja enemypattern y background movil

import pygame
import funcs, vars, chars
from random import choice

global ruta
ruta = None

##j = (1,2,3,4,5)
##i = choice(j)
# ~ i = 1
# ~ ruta = 'rutafinal%d.png' %i
print(ruta)
vars.ruta = ruta

class enemySpawner():
    def __init__(self):
##        self.sprite = funcs.loadImage('enemyPattern.png', 0)
        self.sprite = funcs.loadImage(ruta, 0)
        self.height = self.sprite.get_height()
        self.width = self.sprite.get_width()

        self.timer = 0

    def update(self):
        self.timer += 1.0
##        self.xPixel = (self.timer / (vars.fpsLimit/2))
        self.xPixel = (self.timer / 40)
        vars.forward = self.xPixel
        if self.xPixel == int(self.xPixel):
            if self.xPixel < self.width:
                for yPixel in range(self.sprite.get_height()):
                    if self.sprite.get_at((int(self.xPixel), int(yPixel))) == (0,0,0):
                        vars.enemyList1.append(chars.enemyRock(vars.width, yPixel * 50))
                    if self.sprite.get_at((int(self.xPixel), int(yPixel))) == (255,0,0):
                        vars.enemyList2.append(chars.enemyUFO(vars.width, yPixel * 50))
                    if self.sprite.get_at((int(self.xPixel), int(yPixel))) == (0,255,0):
                        vars.enemyList2.append(chars.enemyRubble(vars.width, yPixel * 50))
                    if self.sprite.get_at((int(self.xPixel), int(yPixel))) == (0,0,255):
                        vars.enemyList3.append(chars.enemyShooter(vars.width, yPixel * 50))
                    if self.sprite.get_at((int(self.xPixel), int(yPixel))) == (255,255,0):
                        vars.ttl = 1
                        vars.powerupList.append(chars.powerupMultishot(vars.width, yPixel * 50))
                    if self.sprite.get_at((int(self.xPixel), int(yPixel))) == (0,255,255):
                        vars.ttl = 2
                        vars.powerupList.append(chars.powerupMultishot(vars.width, yPixel * 50))

class background():
    def __init__(self):
        self.sprite = funcs.loadImage('background.png', 0)
        self.xPos = 0
        self.yPos = 0
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height() 

    def update(self):
        self.xPos -= 1
        if self.xPos <= 0 - self.width:
            self.xPos = 0

    def draw(self):
        vars.screen.blit(self.sprite, (self.xPos, self.yPos))
        vars.screen.blit(self.sprite, (self.xPos + self.width,  self.yPos))
