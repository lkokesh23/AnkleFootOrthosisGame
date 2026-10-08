import pygame
import funcs, vars, chars, misc, main
from random import choice


def main1():

##    vars.points = 0
    b = max(vars.forwardList)
    funcs.printText("Aciertos, Avance, Choques:  " + str(vars.points)+ '  '+ str(b)+ '  '+ str(vars.choques) + "      Wait to replay", 22, -1, -1, (155,155,155))
    funcs.printText("Por favor permanezca derecho mirando la X por 20 segundos en", 22, -1, 350, (155,155,155))
    funcs.printText(str(int(main.time1))+" Segundos", 22, -1, 400, (155,155,155))
    pygame.display.flip()
    vars.screen.fill((0,0,0))
    




    
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            vars.runGame = False
        #~ elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            #~ j = (1,2,3,4,5,6,7,8,9,10)
            #~ i = choice(j)
            i = 1
            #~ vars.points = 0
            #~ vars.choques = 0
            #~ vars.forward = 0
            #~ misc.ruta = 'rutafinal%d.png' %i
            #~ main.time1 = 0
            #~ chars.i= 0
            #~ vars.mainChar.__init__()
            #~ vars.background.__init__()
            #~ vars.enemySpawner.__init__()
            #~ del vars.powerupList[:]
            #~ del vars.enemyList1[:]
            #~ del vars.enemyList2[:]
            #~ del vars.enemyList3[:]		
            #~ del vars.bulletList1[:]
            #~ del vars.bulletList2[:]
            #~ del vars.bulletList3[:]
            #~ vars.gameScreen = 'game'


