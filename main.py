import vars, funcs, game, gameOver, gameOver2, misc
from random import choice

global time1

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
	# ~ j = (1,2,3)#(1,2,3,4,5,6,7,8,9,10)
	# ~ i = choice(j)
	if vars.gameLevel == "facil": # # "medio","dificil"
		j = (0,1,2,3,4,5,6,7,8,9,10)#(1,2,3,4,5,6,7,8,9,10)
		i = choice(j)
		# ~ i = 4
		vars.auto = 'ad%d.txt' %i
		misc.ruta = 'ad%d.png' %i
			
	elif vars.gameLevel == "medio":
		j = (1,2,3,4,5,6,7,8,9)#(1,2,3,4,5,6,7,8,9,10)
		i = choice(j)
		vars.auto = 'rutafinal%d.txt' %i
		misc.ruta = 'rutafinal%d.png' %i
	else:
		j = (10,11,12,13,14,15)#(1,2,3,4,5,6,7,8,9,10)
		i = choice(j)
		vars.auto = 'rutafinal%d.txt' %i
		misc.ruta = 'rutafinal%d.png' %i
	print(misc.ruta)
	vars.auto = 'xpos%d.txt' %i
	vars.e = 0
####                i = 1
	misc.ruta = 'ad%d.png' %i
	pathbalas = ['uno']
	vars.pathbala = choice(pathbalas)
	funcs.startGame(vars.width, vars.height, vars.caption)
	vars.rungame = True
	vars.gameinit = False
	#Game Loop
	# ~ while vars.runGame:
	# ~ time2 = vars.clock.get_time()
	# ~ time1 +=time2
	
def main():
	# ~ time2 = vars.clock.get_time()
	while vars.runGame:
		time1 = vars.time
		game.main()
	# ~ print time1
	# ~ if time1 > duration and it == numtrials-1:# fin del tiempo y trials
		# ~ vars.forwardList.append(vars.forward)
		# ~ vars.rungame = False
		# ~ vars.gameScreen = 'game over 2'
		# ~ vars.f.close()
		# ~ break
	# ~ if time1 > duration and it < numtrials-1:# fin del tiempo 
		# ~ vars.forwardList.append(vars.forward)
		# ~ vars.gameScreen = 'game over 2'
		# ~ #~ vars.rungame = False
		# ~ #~ time1 = 0	
		# ~ #~ continue			
	# ~ if time1 > duration2:# fin del tiempo de descanso
		# ~ it += 1
		# ~ vars.it = it
		# ~ #~ vars.rungame = False
		# ~ #~ gameOver.main()
		# ~ vars.gameScreen = 'game over'
		# ~ time1 = 0
		# ~ #~ continue
	# ~ if vars.gameScreen == 'game':
		# ~ game.main()
	# ~ elif vars.gameScreen == 'game over':
		# ~ gameOver.main()
	# ~ elif vars.gameScreen == 'game over 2':
		# ~ gameOver2.main1()
	##            break;
	##            continue;
