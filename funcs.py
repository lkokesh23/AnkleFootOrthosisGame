import pygame, os, math
from pygame.locals import *
import vars, chars, misc


def startGame(width, height, caption):
    #setup pygame
    pygame.init()
    pygame.font.init()
    # pygame.mixer.init()
    # ~ joystick = pygame.joystick.Joystick(0)
    # ~ joystick.init()

    #setup screen
    #~ vars.screen = pygame.display.set_mode((width, height), FULLSCREEN |DOUBLEBUF |RLEACCEL,32)
    # ~ vars.screen = pygame.display.set_mode((width, height))
    # ~ pygame.display.set_caption(caption)

    #setup clock
    # ~ vars.clock = pygame.time.Clock()


    #setup vars
    vars.mainChar = chars.player()

    vars.enemySpawner = misc.enemySpawner()
    vars.background = misc.background()  
    # ~ vars.joystick = pygame.joystick.Joystick(0)

# Funcion para la lectura de los ficheros
def readdata(nombre,e):
    file=open(nombre,'r')
    contenido=file.readlines()
    j = len(contenido)
    dato1=[]
    dato2=[]
    dato1=contenido[e].find('\t')
    dato2=contenido[e].find('\t',dato1+1)
    valor1=float(contenido[e][0:dato1]) 
    valor2=float(contenido[e][dato1+1:dato2])
    return valor1,valor2

def printText(inputText, inputSize, inputX, inputY, inputColor):
    font = pygame.font.Font(None, inputSize)
    text = font.render((str(inputText)), 1, inputColor)
    if inputX == -1:
        xPos = vars.width/2
    else:
        xPos = inputX
    if inputY == -1:
        yPos = vars.height/2
    else:
        yPos = inputY
    textPosition = text.get_rect(centerx = xPos, centery = yPos)
    vars.screen.blit(text, textPosition)


#eliminar

def loadImage(inputFile, inputColourKey):
    fileLocation = os.path.join('res', inputFile)
    image = pygame.image.load(fileLocation)
    if inputColourKey == -1:
        image.set_colorkey(image.get_at((0,0)))
    elif not inputColourKey == 0:
        image.set_colorkey(inputColourKey)
    image = image.convert()
    return image

###########################################################
#arreglar para joystick
	


#def keyPressed(inputKey):
#    keysPressed = pygame.key.get_pressed()
#    if keysPressed[inputKey]:
#        return True
#    else:
#        return False


#def joystick(axis_x, axis_y, axis_z):
#	axis_x = joystick.get_axis(0)
#	axis_y = joystick.get_axis(1)
#	axis_z = joystick.get_axis(4)

def checkCollision(inputObject1, inputObject2):###PB 6/3/2021
    if inputObject1.xPos + (inputObject1.width-5)  >= inputObject2.xPos and inputObject1.xPos <= inputObject2.xPos + (inputObject2.width-5):
        if inputObject1.yPos + (inputObject1.height-5)  >= inputObject2.yPos and inputObject1.yPos <= inputObject2.yPos + (inputObject2.height-5):
            return True
        else:
            return False
    else:
        return False
