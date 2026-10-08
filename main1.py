# use pygame == 1.9.6    pip3 install pygame==1.9.6 pip3 install warble==1.1.0    pip3 install metawear==0.7.0
# websocket-client==1.1.0
import pygame
import sys
 
from pygame.locals import *
from random import choice
import calibracion, Juego1, Juego3
from time import strftime,localtime,time,gmtime,sleep
# ~ from sensor2 import Sensor
import socket,pickle
sys.path.insert(0, "lib")
import vars,main,game,gameOver
from math import floor
import csv

 
# opening the CSV file


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ~ s.setblocking(False)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sleep(2)


connected = False
print("Server not connected")

# ~ with open('pacientes.csv', mode ='r')as file1:
   
  # ~ # reading the CSV file
  # ~ csvFile1 = csv.reader(file1)
 
  # ~ # displaying the contents of the CSV file
  # ~ for lines1 in csvFile1:
        # ~ print(lines1)

# ~ # opening the CSV file
# ~ with open('dof.csv', mode ='r')as file1:
   
  # ~ # reading the CSV file
  # ~ csvFile2 = csv.reader(file2)
 
  # ~ # displaying the contents of the CSV file
  # ~ for lines2 in csvFile2:
        # ~ print(lines2)
name1 = input("Enter Participant ID (e.g. ANKLE_101,102,... for PD, ANKLE_201,202... for older HC, Participant_0001,0002,..for young HC )  :")
name2 = input("Enter  the foot side information (R or L) :")
name2b = input("Enter the block (pre, training or post): ")

if name2b.lower() in ["pre","post"]:
	name3 = 'prepost'#input("ingresa el nombre del csv a utilizar sin la extension () :")
	print(name3)
elif name2b.lower() in ["training"]:
	name3 = 'pt_rt'#input("ingresa el nombre del csv a utilizar sin la extension () :")
	print(name3)
else:
	name2b = input("Please reEnter the block (pre, training or post): ")
	if name2b.lower() in ["pre","post"]:
		name3 = 'prepost'#input("ingresa el nombre del csv a utilizar sin la extension () :")
		print(name3)
	elif name2b.lower() in ["training"]:
		name3 = 'pt_rt'#input("ingresa el nombre del csv a utilizar sin la extension () :")
		print(name3)
	else:
		sys.exit("incorrect block name")
name4 = 'pt_rt2'

name = name1 +"_"+name2 +"_"+name2b
vars.archivo = name3 +".csv"
vars.archivo2 = name4 +".csv"




# ~ s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ~ s.connect((HOST, PORT))



# ~ print(repr(data_arr))






# nombre del archivo (input nombre apellido + fecha +hora)

start_time1 = time()### add by PB 02 22 2014
date1=strftime("%d.%m.%Y", localtime(start_time1))### add by PB 02 22 2014
time1=strftime("%H:%M:%S", localtime(start_time1))### add by PB 02 22 2014

vars.nombre = (name +"_"+ date1[0:2] + date1[3:5] + date1[6:10] + time1[0:2] + time1[3:5] + time1[6:8])

#~ vars.nombre = raw_input("nombre_EDF: ").replace('\r', '')
vars.f0 = open('./files/'+vars.nombre+'calibracion.txt','a')
vars.f1 = open('./files/'+vars.nombre+'juego1.txt','a', newline='')
vars.f2 = open('./files/'+vars.nombre+'juego2.txt','a')
vars.f3 = open('./files/'+vars.nombre+'juego3.txt','a', newline='')

white = (255,255,255)
black = (0,0,0)
options = ("calibrar","juego1","juego2","juego3")
nivel = ("facil","medio","dificil")
position = [x * 150 + 150 for x in range(len(options))]
position2 = [x * 100 + 250 for x in range(len(nivel))]
# ~ print(position2)
# ~ time1 = 0.0
# ~ w= 1366 
# ~ h= 768



				
class Pane(object):


	def __init__(self):
		pygame.init()
		vars.font = pygame.font.SysFont('Arial', 25)
		pygame.display.set_caption(vars.caption)
		#setup clock
		vars.clock = pygame.time.Clock()
		# ~ vars.screen = pygame.display.set_mode((width, height), FULLSCREEN |DOUBLEBUF |RLEACCEL,32)
		vars.screen = pygame.display.set_mode((vars.width,vars.height), DOUBLEBUF , 32)
		vars.screen.fill((white))
		# ~ calibracion.init()
		
		# ~ Juego1.init()

		
		
		# ~ pygame.display.update()


	def addRect(self,color,xo,yo,wr,hr):
		self.rect = pygame.draw.rect(vars.screen, color, (xo, yo, wr, hr), 2)
		# ~ pygame.display.update()
		#pygame.draw.rect(screen, color, (x,y,width,height), thickness) 

	def addText(self,color,xo,yo,text):
		vars.screen.blit(vars.font.render(text, True, color), (xo, yo))
		# ~ pygame.display.update()

if __name__ == '__main__':
	Pan3 = Pane()
	xr = 0
	xp = 10
	yr = 100
	yp = 10
	ise = None
	ise2 = None
	# ~ xe =0
	# ~ ye=0

	mr = 0
	mr2 = False
	for i in range(len(options)):
		xr= position[i]
		wr = 100
		hr = 100
		color = black
		Pan3.addRect(color,xr,yr,wr,hr)
		text = options[i]
		Pan3.addText(color,xr+xp,yr+yp ,text)	

# ~ vars.sensores.append(Sensor('DB:79:B9:19:22:6A'))	





cimu = 0
while vars.runGame :
	cimu +=1
	vars.clock.tick_busy_loop(100)
	time2 = vars.clock.get_time()
	vars.time += time2
	# ~ vars.e1 = vars.sensores[0].getRoll()
	# ~ print(vars.time)
	
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			s.close()
			pygame.quit(); sys.exit();
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				s.close()
				exit()
			elif event.key == K_ESCAPE:
				vars.gameinit2 = False
				vars.gameinit = False
				vars.gameScreen == 'menu'
			elif event.key == K_s:
				vars.showSquare = not vars.showSquare
			elif event.key == K_j:
				vars.showSine = not vars.showSine
			elif event.key == K_p:
				vars.pause = not vars.pause
				vars.stepb = 0
			elif event.key == K_UP:
				vars.AMPLITUDE += 5	
			elif event.key == K_DOWN:
				vars.AMPLITUDE -= 5	
			elif event.key == K_LEFT:
				vars.step -= 0.001	
			elif event.key == K_RIGHT:
				vars.step += 0.001	
			elif event.key == K_u:
				vars.factor += 0.1	
			elif event.key == K_d:
				vars.factor -= 0.1	
			elif event.key == K_a:
				vars.offset += 5	
			elif event.key == K_z:
				vars.offset -= 5
			elif event.key == K_e:
				vars.eje += 1
			elif event.key == K_f:
				vars.flagPres = not vars.flagPres
			elif event.key == K_i:
				vars.zinv = vars.zinv * -1
		elif event.type == 4:
			x = event.pos[0]
			y = event.pos[1]
			# ~ print([x,y])
		elif event.type == pygame.MOUSEBUTTONUP:
			# ~ print("mouse release")
			vars.xemouse=x
			vars.yemouse=y
			# ~ vars.screen.fill((white))
			mr += 1
			mr2 = True
			vars.mc = not vars.mc
	# ~ print(vars.gameScreen)
	

	
	# ~ print(msg)
	# ~ if(not connected):
		# ~ try:
			# ~ s.listen()
			# ~ clientsocket, address = s.accept()
			# ~ print("Server connected")
			# ~ connected = True
		# ~ except:
			# ~ pass
	# ~ else:
	if(not connected):
		try:
			s.connect((HOST, PORT))
			print("Server connected")
			connected = True
		except:
			pass
	else:
		try:
			msg = s.recv(1024)
			data_arr = pickle.loads(msg)
			# ~ data_arr=msgpack.unpackb(msg, raw=False)
			# ~ print(data_arr)
			vars.y0 = float(data_arr[3])
			vars.z0= float(data_arr[2])
			vars.x0 = float(data_arr[1]) % 360
			vars.x2[0] = vars.x2[1]
			vars.x2[1] = vars.x0

			vars.z2[0] = vars.z2[1]
			vars.z2[1] = vars.z0
			y0 = vars.y0
			
			
			vars.y2[0] = vars.y2[1]
			vars.y2[1] = y0
			#change y value by quadrant
			
			quad = 1
			
			# ~ if floor(vars.y2[1]) in range(85,88) and floor(vars.y2[0]) in range(89,91):
				# ~ quad = 1
			# ~ elif floor(vars.y2[1]) in range(-88,-85) and floor(vars.y2[0]) in range(-91,-89):
				# ~ quad = 2
			
			if floor(vars.y0) >= 0 and (floor(vars.x0) in range(155,206)) and quad == 1:
				y0= 180 - vars.y0
				
			elif floor(vars.y0) < 0 and quad == 1 and (floor(vars.x0) in range(0,26) or floor(vars.x0) in range(335,366)):
				y0= 360 + vars.y0 
				
			elif floor(vars.y0) < 0 and (floor(vars.x0) in range(155,206)) and quad == 1:
				y0= 180 -vars.y0
			
			vars.y2[1] = y0

			
			
			# CHANGE z to -360 360 and more
			if floor(vars.z2[1]) in range(330,361) and floor(vars.z2[0]) in range(0,31) and cimu >10:
				vars.zt -= 1
			elif floor(vars.z2[1]) in range(0,31) and floor(vars.z2[0]) in range(330,361) and cimu >10:
				vars.zt += 1
				
			# CHANGE x to -360 360 and more
			if floor(vars.x2[1]) in range(330,361) and floor(vars.x2[0]) in range(0,31) and cimu >10:
				vars.xt -= 1
			elif floor(vars.x2[1]) in range(0,31) and floor(vars.x2[0]) in range(330,361) and cimu >10:
				vars.xt += 1
				

			# CHANGE y to -360 360 and more
			if floor(vars.y2[1]) in range(330,361) and floor(vars.y2[0]) in range(0,31) and cimu >10:
				vars.yt -= 1
			elif floor(vars.y2[1]) in range(0,31) and floor(vars.y2[0]) in range(330,361) and cimu >10:
				vars.yt += 1
			

			vars.y1 = y0 +(360*vars.yt)
			vars.z1 = (vars.z0+(360*vars.zt))* vars.zinv
			vars.x1 = vars.x0 +(360*vars.xt) 
			
			

			
		except:
			print("Server not connected")
			# ~ s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			# ~ connected = False
			# ~ pass	

		# ~ elif floor(vars.z2[1]) in range(-360,-331) and floor(vars.z2[0]) in range(-31,1) and cimu >10:
			# ~ vars.zt += 1
		# ~ elif floor(vars.z2[1]) in range(690,721) and floor(vars.z2[0]) in range(360,391) and cimu >1:
			# ~ vars.zt -= 1
		# ~ elif round(vars.z2[1]) in range(360,361) and round(vars.z2[0]) in range(690,721) and cimu >1:
			# ~ vars.zt += 1
		# ~ print(vars.y1)
		# ~ print(vars.x0) #problema con  de 0 a -1 valor 359(0 1)   y de 0 a 1 valor 0  (0 1)
		

			
	# ~ print("valup "+str(vars.valup))	
	# ~ print("eje "+str(vars.eje))

	if vars.gameScreen == 'juego1':
		
		if vars.gameinit:
			vars.timeonset= vars.time
			gami1 = Juego1.gaming1()
		if vars.gameinit2:
			vars.screen.fill((white))
			
			gami1.main()
			# ~ if vars.gameLevel == 1:
				# ~ hace algo
			# ~ elif vars.gameLevel == 2:
				# ~ hace algo
			# ~ elif vars.gameLevel == 3:
				# ~ hace algo
			# ~ else:
				# ~ hace algo
			
		else:
			vars.gameinit = False
			vars.screen.fill((white))
			vars.gameScreen = 'menu'
		pygame.display.update()
			
	elif vars.gameScreen == 'juego2':	
		if vars.gameinit:
			vars.timeonset= vars.time
			game.init()
		if vars.time -vars.timeonset<90000 and vars.gameinit2:
			# ~ vars.screen.fill((white))
			if vars.gameScreen2 == 'game':
				game.main()
				game.main2()
			elif vars.gameScreen2 == 'game over':
				gameOver.main()

			# ~ main.main()
			
		else:
			vars.gameinit = False
			vars.screen.fill((white))
			vars.gameScreen = 'menu'
	elif vars.gameScreen == 'juego3':	
		if vars.gameinit:
			vars.timeonset= vars.time
			gami1 = Juego3.gaming1()
		if vars.gameinit2:
			vars.screen.fill((white))
			
			gami1.main()
			# ~ if vars.gameLevel == 1:
				# ~ hace algo
			# ~ elif vars.gameLevel == 2:
				# ~ hace algo
			# ~ elif vars.gameLevel == 3:
				# ~ hace algo
			# ~ else:
				# ~ hace algo
			
		else:
			vars.gameinit = False
			vars.screen.fill((white))
			vars.gameScreen = 'menu'
		pygame.display.update()
	elif vars.gameScreen == 'calibrar':
		if vars.gameinit:
			cali1 = calibracion.calibra()	
			
		if vars.gameinit2:	
			vars.screen.fill((white))
			cali1.main()
		else:
			cali1.main2()
			vars.gameinit = False
			vars.screen.fill((white))
			vars.gameScreen = 'menu'					
		pygame.display.update()				
	elif vars.gameScreen == 'menu':
		if not vars.gameinit:
			mr = 0
			mr2 = False	
			vars.gameinit=1
		hr2 = 50			
		if mr2:
			if mr == 1:
				for i in range(len(options)):
					xr = position[i]
					wr = 100
					hr = 100
					color = black
					Pan3.addRect(color,xr,yr,wr,hr)
					text = options[i]
					Pan3.addText(color,xr+xp,yr+yp ,text)	
					

					if (vars.xemouse >= xr and vars.xemouse <= xr+wr) and (vars.yemouse >= yr and vars.yemouse <= yr+hr) :
						ise = i
						# ~ vars.gameScreen = options[ise]
						if i == 0:
							mr=0
							mr2=False
							print([ise,ise2])
							vars.gameScreen = options[ise]
							continue				
						for i2 in range(len(nivel)):
							yr2 = position2[i2]
							# ~ color = black
							
							Pan3.addRect(color,xr,yr2,wr,hr2)
							text = nivel[i2]
							Pan3.addText(color,xr+xp,yr2+yp ,text)						
				mr2 = False		
					
					# ~ mr = True
			elif mr == 2 :	
				for i in range(len(options)):
					xr= position[i]
					wr = 100
					hr = 100
					color = black
					Pan3.addRect(color,xr,yr,wr,hr)
					text = options[i]
					Pan3.addText(color,xr+xp,yr+yp ,text)
					for i2 in range(len(nivel)):	
						yr2 = position2[i2]	
						if (x >= xr and x <= xr+wr) and (y >= yr2 and y <= yr2+hr2):			
						
							# ~ yr2 = position2[i2]
							
							ise2 = i2	
							if i2 == ise2:
								color = (255,0,0)
							else:
								color = black	
						
							Pan3.addRect(color,xr,yr2,wr,hr2)
							text = nivel[i2]
							Pan3.addText(color,xr+xp,yr2+yp ,text)					
				mr2 = False
				mr = 0
				print([ise,ise2])
				if isinstance(ise, int) and isinstance(ise2, int):
					vars.gameScreen = options[ise]
					vars.gameLevel = nivel[ise2]
					
					ise = None
					ise2 = None
			else:
				for i in range(len(options)):
					xr= position[i]
					wr = 100
					hr = 100
					color = black
					Pan3.addRect(color,xr,yr,wr,hr)
					text = options[i]
					Pan3.addText(color,xr+xp,yr+yp ,text)
			
		pygame.display.update()	

		


