import pygame, math, random
import vars, funcs, main, game
from pygame.locals import *

global axis_z
axis_z= None
i = 0
global vel
vel = 1


#Main Player

class player():
	def __init__(self):
	
		self.sprite = funcs.loadImage('char.png', -1)

		self.xm = vars.width/2
		self.ym = vars.height/2
		self.xPos = self.xm
		self.yPos = self.ym
		self.width = self.sprite.get_width()
		self.height = self.sprite.get_height()

		self.speed = 2
		self.yback =0

		self.reloadTime = 300
		self.reloadTimer = 0

		self.powerUpTime = 100
		self.powerUpTimer = 0

		self.powerUp = 'none'
		# ~ vars.f = open(vars.nombre+'.txt','a')
#control con teclado cambiar por joystick
	def update(self):
		timer = game.time1
		#~ b = funcs.readdata(vars.auto,vars.e)
		#~ vars.e += 1
		self.xPos= int(vars.width/2)
		
		if vars.eje == 0:
			vars.y1b= vars.x1
		elif vars.eje == 1:	
			vars.y1b= vars.y1
		elif vars.eje == 2:	
			vars.y1b= vars.z1
		elif vars.eje > 2:
			vars.eje = 0
		# ~ print(vars.eje)	
		# ~ vars.y1b= vars.z1	
		
		val50 = (vars.valup-vars.valdo)/2.0
		# ~ val=0.1
		# ~ try:
		if val50 == 0:
			vars.screen.fill((255,255,255))
			vars.screen.blit(vars.font.render("calibrar primero", True, (0,0,0)), (100, 100))
			val50 = 0.001
			vars.gameinit = False
			
			vars.gameScreen = 'menu'				
		
		# ~ vars.y1b = vars.y1b-val50
		vars.factor = 0.75	
		if vars.y1b > -500 and vars.y1b < 500:
			# ~ val1 = int(((vars.AMPLITUDE/2)/val50)*vars.y1b)
			val = ((vars.height/2)/(abs((val50)*vars.factor)))*(vars.y1b-(vars.valup -val50))
			val2 = int(val+vars.offset)
			val1 = (vars.height/2)-val2
			self.yback = val1
			# ~ print(vars.y1b)	
			# ~ print(val2)
			# ~ print(val1)
		else:
			val1 = self.yback
			# ~ val = ((self.AMPLITUDE/2)/val50)*vars.y1b
			# ~ val= self.xm-val1		
		#self.yPos= int(vars.height/2)+val1 #PB 28 01 2020
		self.yPos = val1
		# ~ axis_x = vars.x1
		# ~ axis_y = vars.y1
		axis_z = vars.z1
		# ~ axis_x = vars.joystick.get_axis(0)
		# ~ axis_y = vars.joystick.get_axis(1)
		# ~ axis_z = vars.joystick.get_axis(3)
##        if (not self.yPos + self.height > vars.height) and axis_x < -0.2:
##            self.yPos += self.speed
##        elif (not self.yPos < 0) and axis_x > 0.2:
##            self.yPos -= self.speed
##
##        if (not self.xPos + self.width > vars.width) and axis_y < -0.2:
##            self.xPos += self.speed
##        elif (not self.xPos < 0) and axis_y > 0.2:
##            self.xPos -= self.speed


		#~ deg = math.pi/2
		# ~ deg = 0
		# ~ cos = math.cos(deg)
		# ~ sin = math.sin(deg)


		
		# ~ if  axis_y > 0.1:
# ~ ##            self.yPos += self.speed * axis_y
			# ~ self.yPos += cos * axis_y * self.speed
			# ~ self.xPos += sin * axis_y * self.speed

			
		# ~ elif axis_y < -0.1:
# ~ ##            self.yPos -= self.speed * -axis_y
			# ~ self.yPos += cos * axis_y * self.speed
			# ~ self.xPos += sin * axis_y * self.speed

		# ~ if axis_x > 0.1:
# ~ ##            self.xPos -= self.speed * -axis_x         
			# ~ self.xPos += cos * axis_x * self.speed
			# ~ self.yPos -= sin * axis_x * self.speed
			
		# ~ elif axis_x < -0.1:
# ~ ##            self.xPos -= self.speed * -axis_x
			# ~ self.xPos += cos * axis_x * self.speed
			# ~ self.yPos -= sin * axis_x * self.speed


		# ~ if (self.yPos + self.height > vars.height):
			# ~ self.yPos = vars.height - self.height 
		# ~ elif (self.yPos <= 0):
			# ~ self.yPos = 0
		# ~ if(self.xPos + self.width > vars.width):
			# ~ self.xPos = vars.width - self.width
		# ~ elif (self.xPos <= 0):
			# ~ self.xPos = 0

		# ~ print(self.yPos)

		if self.reloadTimer < self.reloadTime:
			self.reloadTimer += 1

		if not self.powerUp == 'none':
			if self.powerUpTimer < self.powerUpTime:
				self.powerUpTimer += 1
			else:
				self.powerUp = 'none'
				self.powerUpTimer = 0

		if axis_z >= -0.02 :
			self.umbral = 1
			self.reloadTimer = 0

## se crea esta condicion pasra que no caiga el juego por empezar con palanca 2 arriba

		if axis_z < -0.02 and timer<1000:
			self.umbral = 1
			self.reloadTimer = 0

		n1= -0.02;
		n2= -0.2;
		n3= -0.4;
		n4= -0.6
	

	
		if vars.pathbala == 'uno':
			funcs.printText("Trial   %s   " %vars.it + "Balas:  " + '1,2,3   '+"Puntos:  " + (str(vars.points)), 22, -1, 10, (0,255,0))
			if axis_z < n1 and axis_z > n2 and self.reloadTimer >= 20:
				if self.powerUp  == 'none' and self.umbral==1 :

					vars.bulletList1.append(bulletSimple1(self.xPos, self.yPos + ((self.height / 2) - 1), 0))
				self.umbral=0
				self.reloadTimer = 0


			if axis_z < n2 and axis_z > n3 and self.reloadTimer >= 20:
				if self.powerUp == 'none' and self.umbral==1 :
				   
					vars.bulletList2.append(bulletSimple2(self.xPos, self.yPos + ((self.height / 2) - 1), 0))
				self.umbral=0
				self.reloadTimer = 0



			if axis_z < n3 and axis_z > n4 and self.reloadTimer >= 20:
				if self.powerUp == 'none' and self.umbral==1 :
									 
					vars.bulletList3.append(bulletSimple3(self.xPos, self.yPos + ((self.height / 2) - 1), 0))
				self.umbral=0
				self.reloadTimer = 0

			if axis_z < n4:
				self.umbral=0


		if vars.pathbala == 'dos':
##            funcs.printText("Balas:  " + 'vars.pathbala' + '\t' +"Puntos:  " + vars.points, 22, -1, 10, (0,255,0))
			funcs.printText("Balas:  " + '2,3,1   ' +"Puntos:  " + (str(vars.points)), 22, -1, 10, (0,255,0))

			if axis_z < n1 and axis_z > n2 and self.reloadTimer >= 20:         
				if self.powerUp  == 'none' and self.umbral==1 :
									 
					vars.bulletList2.append(bulletSimple2(self.xPos, self.yPos + ((self.height / 2) - 1), 0))
				self.umbral=0
				self.reloadTimer = 0

			if axis_z < n2 and axis_z > n3 and self.reloadTimer >= 20:
				if self.powerUp == 'none' and self.umbral==1 :
									  
					vars.bulletList3.append(bulletSimple3(self.xPos, self.yPos + ((self.height / 2) - 1), 0))
				self.umbral=0
				self.reloadTimer = 0


			if axis_z < n3 and axis_z > n4 and self.reloadTimer >= 20:
				if self.powerUp == 'none' and self.umbral==1 :
					   
					vars.bulletList1.append(bulletSimple1(self.xPos, self.yPos + ((self.height / 2) - 1), 0))
				self.umbral=0
				self.reloadTimer = 0

			if axis_z < n4:
				self.umbral=0




		if vars.pathbala == 'tres':
##            funcs.printText("Balas:  " + 'vars.pathbala' + '\t' +"Puntos:  " + vars.points , 22, -1, 10, (0,255,0))
			funcs.printText("Balas:  " + '3,1,2   ' +"Puntos:  " + (str(vars.points)), 22, -1, 10, (0,255,0))
			if axis_z < n1 and axis_z > n2 and self.reloadTimer >= 20:         
				if self.powerUp  == 'none' and self.umbral==1 :
						  
					vars.bulletList3.append(bulletSimple3(self.xPos, self.yPos + ((self.height / 2) - 1), 0))
				self.umbral=0
				self.reloadTimer = 0

			if axis_z < n2 and axis_z > n3 and self.reloadTimer >= 20:
				if self.powerUp == 'none' and self.umbral==1 :
								
					vars.bulletList1.append(bulletSimple1(self.xPos, self.yPos + ((self.height / 2) - 1), 0))
				self.umbral=0
				self.reloadTimer = 0


			if axis_z < n3 and axis_z > n4 and self.reloadTimer >= 20:
				if self.powerUp == 'none' and self.umbral==1 :
							
					vars.bulletList2.append(bulletSimple2(self.xPos, self.yPos + ((self.height / 2) - 1), 0))
				self.umbral=0
				self.reloadTimer = 0

			if axis_z < n4:
				self.umbral=0

## graba los datos del movimiento

	#~ vars.f.write((str(timer))+'\t'+(str(self.xPos))+'\t'+(str(self.yPos))+'\t'+ (str(axis_z))+'\n')

		# ~ vars.f.write((str(vars.time))+'\t'+(str(timer))+'\t'+(str(self.xPos))+'\t'+(str(self.yPos)) + '\t'+(str(vars.forward))+'\t'+(str(vars.choques))+'\n')            
		vars.f2.write("juego2" +'\t'+ vars.gameLevel +'\t'+ str(vars.it)  +'\t'+ vars.auto +'\t'+(str(vars.time))+'\t'+(str(vars.timer))+'\t'+(str(self.xPos))+'\t'+(str(self.yPos)) + '\t'+(str(vars.forward))+'\t'+(str(vars.choques))+'\t'+(str(vars.x1))+'\t'+(str(vars.y1))+'\t'+(str(vars.z1))+'\n') ##PB 27 12 19

	def draw(self):
		vars.screen.blit(self.sprite, (self.xPos,  self.yPos))


#Bullet Types
class bulletSimple1():
	def __init__(self, inputX, inputY, inputYSpeed):
		self.sprite = funcs.loadImage('bullet1.png', 0)
		self.xPos = inputX
		self.yPos = inputY

		self.width = self.sprite.get_width()
		self.height = self.sprite.get_height()
		
		self.ySpeed = inputYSpeed
		self.speed = 3

	def update(self):
		self.xPos += self.speed
		self.yPos += self.ySpeed

	def draw(self):
		vars.screen.blit(self.sprite, (self.xPos,  self.yPos))

	def checkState(self):
		if self.xPos > vars.width + self.width:
			return 'delete'

class bulletSimple2():
	def __init__(self, inputX, inputY, inputYSpeed):
		self.sprite = funcs.loadImage('bullet2s.png', -1)

		self.xPos = inputX
		self.yPos = inputY

		self.width = self.sprite.get_width()
		self.height = self.sprite.get_height()
		
		self.ySpeed = inputYSpeed
		self.speed = 3

	def update(self):
		self.xPos += self.speed
		self.yPos += self.ySpeed

	def draw(self):
		vars.screen.blit(self.sprite, (self.xPos,  self.yPos))

	def checkState(self):
		if self.xPos > vars.width + self.width:
			return 'delete'

class bulletSimple3():
	def __init__(self, inputX, inputY, inputYSpeed):
		self.sprite = funcs.loadImage('bullet3s.png', -1)

		self.xPos = inputX
		self.yPos = inputY

		self.width = self.sprite.get_width()
		self.height = self.sprite.get_height()
		
		self.ySpeed = inputYSpeed
		self.speed = 3

	def update(self):
		self.xPos += self.speed
		self.yPos += self.ySpeed

	def draw(self):
		vars.screen.blit(self.sprite, (self.xPos,  self.yPos))

	def checkState(self):
		if self.xPos > vars.width + self.width:
			return 'delete'


class enemyBulletSimple():
	def __init__(self, inputX, inputY):
		self.sprite = funcs.loadImage('bullet2.png', -1)

		self.xPos = inputX
		self.yPos = inputY

		self.width = self.sprite.get_width()
		self.height = self.sprite.get_height()

		self.speed = 3
		self.lives = 10

	def update(self):
		self.xPos -= self.speed

	def draw(self):
		vars.screen.blit(self.sprite, (self.xPos,  self.yPos))

	def checkState(self):
		if self.xPos < 0 - self.width:
			return 'delete'


#Powerups

class powerupMultishot():
	def __init__(self, inputX, inputY):

		if vars.ttl == 1:
			self.sprite = funcs.loadImage('powerup1.png', -1)#-1
			
		if vars.ttl == 2:
			self.sprite = funcs.loadImage('powerup2.png', 0)
##            
##        if vars.ttl == 3:
##            self.sprite = funcs.loadImage('powerup3.png', 0)
##
##        if vars.ttl == 4:
##            self.sprite = funcs.loadImage('powerup4.png', 0)

##        print vars.ttl    
		self.xPos = inputX
		self.yPos = inputY

		self.width = self.sprite.get_width()
		self.height = self.sprite.get_height()

		self.speed = vel

	def update(self):
		self.xPos -= self.speed

	def draw(self):
		vars.screen.blit(self.sprite, (self.xPos,  self.yPos))

	def checkState(self):
		if self.xPos < 0 - self.width:
			return 'delete'

		

#Enemies


class enemyRock():
	def __init__(self, inputX, inputY):
		self.sprite1 = funcs.loadImage('enemy1.png', -1)
		self.width = self.sprite1.get_width()
		self.height = self.sprite1.get_height()
		self.xPos = inputX
		self.yPos = inputY

		self.speed = vel
		self.lives = 1

	def update(self):
		self.xPos -= self.speed

	def draw(self):
		if self.lives == 1:
			vars.screen.blit(self.sprite1, (self.xPos,  self.yPos))
			
	def checkState(self):
		if self.xPos < 0 - self.width:
			return 'delete'

class enemyUFO():
	def __init__(self, inputX, inputY):
		self.sprite = funcs.loadImage('enemy2.png', -1)
		self.width = self.sprite.get_width()
		self.height = self.sprite.get_height()
		self.xPos = inputX
		self.yPos = inputY
		self.originalYPos = inputY

		self.speed = vel
		self.lives = 1

	def update(self):
		self.xPos -= self.speed
		self.yPos = 60*math.sin(0.03*self.xPos)+ self.originalYPos

	def draw(self):
		vars.screen.blit(self.sprite, (self.xPos,  self.yPos))

	def checkState(self):
		if self.xPos < 0 - self.width:
			return 'delete'

class enemyRubble():
	def __init__(self, inputX, inputY):
		self.sprite = funcs.loadImage('enemy3.png', -1)
		self.width = self.sprite.get_width()
		self.height = self.sprite.get_height()
		self.xPos = inputX
		self.yPos = inputY

		self.speed = vel
		self.lives = 500

	def update(self):
		self.xPos -= self.speed

	def draw(self):
		vars.screen.blit(self.sprite, (self.xPos,  self.yPos))

	def checkState(self):
		if self.xPos < 0 - self.width:
			return 'delete'

class enemyShooter():
	def __init__(self, inputX, inputY):
		self.sprite = funcs.loadImage('enemy4.png', -1)
		self.width = self.sprite.get_width()
		self.height = self.sprite.get_height()
		self.xPos = inputX
		self.yPos = inputY
		self.originalYPos = inputY

		self.speed = vel
		self.lives = 1

		self.bulletTimer = 0
		self.bulletTime = 70

	def update(self):
		self.xPos -= self.speed
		self.yPos = 100*math.sin(0.02*self.xPos)+ self.originalYPos
		self.bulletTimer += 1
		if self.bulletTimer >= self.bulletTime:
			self.bulletTimer = 0
			vars.enemyList4.append(enemyBulletSimple(self.xPos, self.yPos + ((self.height / 2) - 1)))

	def draw(self):
		vars.screen.blit(self.sprite, (self.xPos,  self.yPos))

	def checkState(self):
		if self.xPos < 0 - self.width:
			return 'delete'

class enemyBoss():
	def __init__(self, inputX, inputY):
		self.sprite1 = funcs.loadImage('enemy5.png', 0)
		self.width = self.sprite1.get_width()
		self.height = self.sprite1.get_height()
		self.xPos = inputX
		self.yPos = inputY

		self.speed = vel
		self.lives = 150

	def update(self):
		self.xPos -= self.speed

 
	def draw(self):
		vars.screen.blit(self.sprite1, (self.xPos,  self.yPos))


	def checkState(self):
		if self.xPos < 0 - self.width:
			return 'delete'
		

