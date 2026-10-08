import pygame
import funcs, vars, misc
from random import choice

def main():
#   vars.points = 0
	if vars.gameLevel == "facil": # # "medio","dificil"
		#j = (0,1,2,3,4,5,6,7,8,9,10)#(1,2,3,4,5,6,7,8,9,10)
		#i = choice(j)
		i = 0
		vars.auto = 'ad%d.txt' %i
		misc.ruta = 'ad%d.png' %i
			
	elif vars.gameLevel == "medio":
		# ~ j = (1,2,3,4,5,6,7,8,9)#(1,2,3,4,5,6,7,8,9,10)
		# ~ i = choice(j)
		i = 1
		vars.auto = 'ruta%d.txt' %i
		misc.ruta = 'ruta%d.png' %i
	else:
		# ~ j = (10,11,12,13,14,15)#(1,2,3,4,5,6,7,8,9,10)
		# ~ i = choice(j)
		i = 2
		vars.auto = 'rutafinal%d.txt' %i
		misc.ruta = 'rutafinal%d.png' %i
	print(misc.ruta)
	vars.mainChar.__init__()
	vars.background.__init__()
	vars.enemySpawner.__init__()
	pathbalas = ['uno']
	vars.pathbala = choice(pathbalas)
	del vars.powerupList[:]
	del vars.enemyList1[:]
	del vars.enemyList2[:]
	del vars.enemyList3[:]      
	del vars.bulletList1[:]
	del vars.bulletList2[:]
	del vars.bulletList3[:]
##    j = (1:10)

	
	vars.gameScreen2 = 'game'   

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			vars.runGame = False


