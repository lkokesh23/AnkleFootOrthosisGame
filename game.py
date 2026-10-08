import pygame
import vars, funcs, misc, chars

from random import choice


def init():
	numtrials = 15
	# ~ vars.nombre = input('ingresa el nombre y apellido:  ')
	it = 0
	global time1
	print('trial %s' %it)
	vars.it =it
	time1 = 0
	duration = 90000
	duration2 = duration + 20000
	if vars.gameLevel == "facil": # # "medio","dificil"
		i = 0#(0,1,2,3,4,5,6,7,8,9,10)#(1,2,3,4,5,6,7,8,9,10)
		#i = choice(j)
		# ~ i = 4
		vars.auto = 'ad%d.txt' %i
		misc.ruta = 'ad%d.png' %i
			
	elif vars.gameLevel == "medio":
		i = 1#(1,2,3,4,5,6,7,8,9)#(1,2,3,4,5,6,7,8,9,10)
		#i = choice(j)
		vars.auto = 'ruta%d.txt' %i
		misc.ruta = 'ruta%d.png' %i
	else:
		i = 2# (10,11,12,13,14,15)#(1,2,3,4,5,6,7,8,9,10)
		#i = choice(j)
		vars.auto = 'rutafinal%d.txt' %i
		misc.ruta = 'rutafinal%d.png' %i
	print(misc.ruta)
	


	vars.e = 0
####                i = 1
	
	pathbalas = ['uno']
	vars.pathbala = choice(pathbalas)
	funcs.startGame(vars.width, vars.height, vars.caption)
	vars.rungame = True
	vars.gameinit = False
	vars.gameinit2 = True
	vars.AMPLITUDE= vars.height
	

def main():
	time1 = vars.time
## limite superior, enemigos1, balas1
	for individualBullet in vars.bulletList1:
		if individualBullet.checkState() == 'delete':
			vars.bulletList1.remove(individualBullet)

		for individualEnemy in vars.enemyList1:	
			if funcs.checkCollision(individualEnemy, individualBullet):
				if individualEnemy.lives > 1:
					individualEnemy.lives -= 1
				else:
					vars.points += 1
					vars.enemyList1.remove(individualEnemy)

				try: vars.bulletList1.remove(individualBullet)
				except: pass
	
		enemyList2y3 = vars.enemyList2 + vars.enemyList3
		for individualEnemy in enemyList2y3:	
			if funcs.checkCollision(individualEnemy, individualBullet):
				try: vars.bulletList1.remove(individualBullet)
				except: pass
		
		##    for individualBullet in vars.bulletList1:
		individualBullet.update()
		individualBullet.draw()

	
	for individualEnemy in vars.enemyList1:
		if individualEnemy.checkState() == 'delete':
			vars.enemyList1.remove(individualEnemy)
		elif funcs.checkCollision(individualEnemy, vars.mainChar):
			vars.choques += 1
			vars.forwardList.append(vars.forward)
			vars.gameScreen2 = "game over"

	for individualEnemy in vars.enemyList1:
		individualEnemy.update()
		individualEnemy.draw()

## limite inferior, enemigos1, balas1

## limite superior, enemigos2, balas2
	for individualBullet in vars.bulletList2:
		if individualBullet.checkState() == 'delete':
			vars.bulletList2.remove(individualBullet)

		for individualEnemy in vars.enemyList2:	
			if funcs.checkCollision(individualEnemy, individualBullet):
				if individualEnemy.lives > 1:
					individualEnemy.lives -= 15
				else:
					vars.points += 1
					vars.enemyList2.remove(individualEnemy)

				try: vars.bulletList2.remove(individualBullet)
				except: pass
	
		enemyList1y3 = vars.enemyList1 + vars.enemyList3
		for individualEnemy in enemyList1y3:	
			if funcs.checkCollision(individualEnemy, individualBullet):
				try: vars.bulletList2.remove(individualBullet)
				except: pass


	
##    for individualBullet in vars.bulletList2:
		individualBullet.update()
		individualBullet.draw()

	
	for individualEnemy in vars.enemyList2:
		if individualEnemy.checkState() == 'delete':
			vars.enemyList2.remove(individualEnemy)
		elif funcs.checkCollision(individualEnemy, vars.mainChar):
			vars.choques += 1
			vars.forwardList.append(vars.forward)
			vars.gameScreen2 = "game over"

	for individualEnemy in vars.enemyList2:
		individualEnemy.update()
		individualEnemy.draw()

## limite inferior, enemigos2, balas2

## limite superior, enemigos3, balas3
	for individualBullet in vars.bulletList3:
		if individualBullet.checkState() == 'delete':
			vars.bulletList3.remove(individualBullet)

		for individualEnemy in vars.enemyList3:	
			if funcs.checkCollision(individualEnemy, individualBullet):
				if individualEnemy.lives > 1:
					individualEnemy.lives -= 30
				else:
					vars.points += 1
					vars.enemyList3.remove(individualEnemy)

				try: vars.bulletList3.remove(individualBullet)
				except: pass
	
		enemyList1y2 = vars.enemyList1 + vars.enemyList2
		for individualEnemy in enemyList1y2:	
			if funcs.checkCollision(individualEnemy, individualBullet):
				try: vars.bulletList3.remove(individualBullet)
				except: pass
	
##    for individualBullet in vars.bulletList3:
		individualBullet.update()
		individualBullet.draw()

	
	for individualEnemy in vars.enemyList3:
		if individualEnemy.checkState() == 'delete':
			vars.enemyList3.remove(individualEnemy)
		elif funcs.checkCollision(individualEnemy, vars.mainChar):
			vars.choques += 1
			vars.forwardList.append(vars.forward)
			vars.gameScreen2 = "game over"


	for individualEnemy in vars.enemyList4:
		if funcs.checkCollision(individualEnemy, vars.mainChar):
			vars.choques += 1
			vars.forwardList.append(vars.forward)
			vars.gameScreen2 = "game over"




##    for individualBullet in vars.bulletList3:
##        for individualPowerup in vars.powerupList:
##            if funcs.checkCollision(individualPowerup, individualBullet):
##                try: del vars.bulletList3[0]
##                except: pass


	enem = vars.enemyList1+vars.enemyList2
	for individualEnemy in vars.enemyList4:
		for individual in enem:
			if funcs.checkCollision(individualEnemy, individual):
##                try: del vars.enemyList4[]
				try: vars.enemyList4.remove(individualEnemy)
				except: pass

	


	enemy = vars.enemyList3 + vars.enemyList4	
	for individualEnemy in enemy:
		individualEnemy.update()
		individualEnemy.draw()



		
## limite inferior, enemigos3, balas3

	for individualPowerup in vars.powerupList:
		if individualPowerup.checkState() == 'delete':
			vars.powerupList.remove(individualPowerup)
		elif funcs.checkCollision(individualPowerup, vars.mainChar):
			vars.powerupList.remove(individualPowerup)
			vars.mainChar.powerUp = 'multishot'

	for individualPowerup in vars.powerupList:
		individualPowerup.update()
		individualPowerup.draw()

	vars.enemySpawner.update()

	vars.mainChar.update()
	vars.mainChar.draw()

##    funcs.printText("Puntaje:  " + str(vars.points), 22, -1, 10, (255,255,255))


	# ~ for event in pygame.event.get():
		# ~ if event.type == pygame.QUIT:
			# ~ vars.runGame = False
		# ~ if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
			# ~ vars.runGame = False	

def main2():
	pygame.display.flip()  #PB
	vars.screen.fill((0,0,0))

	vars.background.update()
	vars.background.draw()

	# ~ vars.clock.tick(vars.fpsLimit) PB
	# print functions.clock.get_fps()
