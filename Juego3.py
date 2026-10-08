import sys, pygame, math, os
from pygame.locals import *
from time import sleep, time
from random import choice
# ~ import numpy as np
sys.path.insert(0, "lib")
import vars
import csv


	# ~ if vars.gameinit:
		# set up a bunch of constants
class gaming1(object):		
	def __init__(self):		
		vars.pause = False
		self.pause_start_time = None
		self.PAUSE_DURATION = 30
		self.WHITE      = (255, 255, 255)
		self.DARKRED    = (255,   200,   200)
		self.RED        = (255,   0,   0)
		self.BLACK      = (  0,   0,   0)
		self.BLUE      = (  0, 0,   255) ### HERE BLUE
		self.LBLUE       = (  200,   200, 255) ### HERE lightBLUE
		self.GREEN      = (  0, 255,   0) ### HERE BLUE

		self.BGCOLOR = self.WHITE

		self.WINDOWWIDTH = vars.width # width of the program's window, in pixels
		self.WINDOWHEIGHT = vars.height # height in pixels
		self.WIN_CENTERX = int(self.WINDOWWIDTH / 2) # the midpoint for the width of the window
		self.WIN_CENTERY = int(self.WINDOWHEIGHT / 2) # the midpoint for the height of the window
		self.data_list3 = [["game","difficulty", "amplitude", "velocity", "time","xpos","y_computer","y_human","y_error","trial","kp","x","y","z"]]
		self.frame_index = 0
		self.trail_stride = 2
		self.trail_max = 350
		self.log_stride = 2

		#FPS = vars.fpsLimit # frames per second to run at


		# Ensure the configuration CSV exists; fall back to sensible defaults if missing.
		# Prefer the user-requested `pt_rt2.csv` first when available.
		archivo2_path = getattr(vars, 'archivo2', None)
		if not archivo2_path or not os.path.exists(archivo2_path):
			# First prefer explicit project candidates (user-requested order)
			for cand in ('pt_rt2.csv', 'pt_rt.csv'):
				if os.path.exists(cand):
					archivo2_path = cand
					print(f"Juego3: using found config file '{archivo2_path}'")
					break
			else:
				# Next, if the block-based default exists, use it
				fallback = getattr(vars, 'archivo', None)
				if fallback and os.path.exists(fallback):
					archivo2_path = fallback
					print(f"Juego3: using fallback config file '{archivo2_path}'")
				# Finally try 'prepost.csv' as last resort
				elif os.path.exists('prepost.csv'):
					archivo2_path = 'prepost.csv'
					print(f"Juego3: using found config file '{archivo2_path}'")
				else:
					raise FileNotFoundError(f"Juego3 config CSV not found: looked for '{vars.archivo2}' and fallbacks")

		with open(archivo2_path) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			line_count = 0
			self.vel = []
			self.amp = []
			self.amp2= []
			self.kp  = []
			self.blocktimes =[0]
			for row in csv_reader:
				if line_count == 0:
					print(f'Column names are {", ".join(row)}')
					line_count += 1
				else:
					# Support 3-column format [vel, amp, kp] or 4-column [vel, amp, amp2, kp]
					if not row or len(row) < 3:
						print(f"Skipping CSV line {line_count}: expected at least 3 columns, got {len(row)}")
						line_count += 1
						continue
					try:
						vel_val = float(row[0])
						amp_val = float(row[1])
						
						# Check if we have 4 columns (vel, amp, amp2, kp) or 3 columns (vel, amp, kp)
						if len(row) >= 4:
							amp2_val = float(row[2])
							kp_val = int(float(row[3]))
						else:
							amp2_val = amp_val  # default amp2 to amp if not provided
							kp_val = int(float(row[2]))
					except Exception as e:
						print(f"CSV parse error on line {line_count}: {e}")
						line_count += 1
						continue

					# append parsed values
					self.vel.append(vel_val)
					self.amp.append(amp_val)
					self.amp2.append(amp2_val)
					self.kp.append(kp_val)
					line_count += 1
			# ~ self.vel.append=self.vel[-1]
			# ~ self.amp.append
		self.total_trials = len(self.vel)
		self.max_trials = 120
		self.effective_trials = min(self.total_trials, self.max_trials)
#Oct 2023
		# ~ if vars.gameLevel == "facil": # # "medio","dificil"
			# ~ vars.AMPLITUDE = choice((80,80,80)) # how many pixels tall the waves with rise/fall.
			# ~ vars.step = choice((0.008,0.008,0.008))
		# ~ elif vars.gameLevel == "medio":
			# ~ vars.AMPLITUDE = choice((80,80,80)) # how many pixels tall the waves with rise/fall.
			# ~ vars.step = choice((0.008,0.008,0.008))
		# ~ else:
			# ~ vars.AMPLITUDE = choice((80,80,80)) # how many pixels tall the waves with rise/fall.
			# ~ vars.step = choice((0.008,0.008,0.008))
#Oct 2023
		# ~ if vars.gameLevel == "facil": # # "medio","dificil"
			# ~ vars.AMPLITUDE = choice((40,50,60)) # how many pixels tall the waves with rise/fall.
			# ~ vars.step = choice((0.004,0.005,0.006))
		# ~ elif vars.gameLevel == "medio":
			# ~ vars.AMPLITUDE = choice((70,80,90)) # how many pixels tall the waves with rise/fall.
			# ~ vars.step = choice((0.007,0.008,0.009))
		# ~ else:
			# ~ vars.AMPLITUDE = choice((100,110,120)) # how many pixels tall the waves with rise/fall.
			# ~ vars.step = choice((0.010,0.011,0.012))

		# standard pygame setup code
		# ~ pygame.init()
		# ~ FPSCLOCK = pygame.time.Clock()
		# ~ DISPLAYSURF = vars.screen #pygame.display.set_mode((WINDOWWIDTH, self.WINDOWHEIGHT))
		# ~ pygame.display.set_caption('Trig Waves')
		self.fontObj = pygame.font.Font('freesansbold.ttf', 16)

		# Background soundtrack
		self.soundtrack = None
		try:
			sound_path = os.path.join(
				os.path.dirname(__file__),
				"assets",
				"game3",
				"sound",
				"soundtrack.mp3",
			)
			self.soundtrack = pygame.mixer.Sound(sound_path)
			self.soundtrack.set_volume(0.2)
			pygame.mixer.Sound.play(self.soundtrack, loops=-1)
		except Exception as e:
			print(f"Juego3: soundtrack not available ({e})")

		# variables that track visibility modes


		# ~ vars.pause = False

		self.xPos = 0
		self.step = 0 # the current input f
		self.contador = 0
		self.count = 0
		self.count2 = 0
		self.contadorb = 0
		self.countb = 0
		self.count2b = 0
		self.block_trial = 0
		self.inittime = vars.time
		self.inittime2 = vars.time

		vars.AMPLITUDE= self.amp[self.contador]
		vars.step = self.vel[self.contador]
		self.AMPLITUDE = vars.AMPLITUDE

		### HERE 
		self.posRecord = {'sin': [], 'square': []} # keeps track of the ball positions for drawing the waves

		# making text Surface and Rect objects for various labels

		### HERE 
		self.squareLabelSurf = self.fontObj.render(' ', True, self.BLUE, self.BGCOLOR)#square
		self.squareLabelRect = self.squareLabelSurf.get_rect()

		self.sinLabelSurf = self.fontObj.render(' ', True, self.RED, self.BGCOLOR)#sin
		self.sinLabelRect = self.sinLabelSurf.get_rect()


		self.instructionsSurf = self.fontObj.render('Esc menu, P pause', True, self.BLACK, self.BGCOLOR)
		self.instructionsRect = self.instructionsSurf.get_rect()
		self.instructionsRect.left = 10
		self.instructionsRect.bottom = self.WINDOWHEIGHT - 10

		### HERE
		self.yPosSquare = 0 #vars.AMPLITUDE # starting position
		self.yback =0
		self.countsin = 0
		self.countsin2 = 0
		vars.gameinit=False
		vars.gameinit2 =True
		
		self.showSquare2 = False
		
		# Generate output filename once at initialization for incremental saving
		self.output_filename = self._generate_filename()
		self.last_saved_index = 0  # Track how much data has been saved
		
		# Pause/Play button properties (top-left area)
		self.button_width = 80
		self.button_height = 50
		
		# Menu button properties (positioned in top-left)
		self.menu_button_width = 70
		self.menu_button_height = 50
		self.menu_button_x = 10
		self.menu_button_y = 10
		self.menu_button_rect = pygame.Rect(self.menu_button_x, self.menu_button_y, self.menu_button_width, self.menu_button_height)
		
		# Pause button positioned to the right of menu button
		self.button_x = self.menu_button_x + self.menu_button_width + 10
		self.button_y = self.menu_button_y
		self.button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)




	def salir(self):        
		print('Exportando datos...')
		for sensor in self.sensores:
			sensor.device.disconnect()
			sleep(1)
		for sensor in self.sensores:
			sensor.exportarDatos('datos_%f.txt' % time())
		print('Exportacion exitosa')
		sys.exit()

	# ~ def quat2euler(q): #z y x
		# ~ #// roll (x-axis rotation)
		# ~ sinr_cosp = +2.0 * (q.w * q.x + q.y * q.z);
		# ~ cosr_cosp = +1.0 - 2.0 * (q.x * q.x + q.y * q.y);
		# ~ anglesroll = math.atan2(sinr_cosp, cosr_cosp);
		
		# ~ #// pitch (y-axis rotation)
		# ~ sinp = +2.0 * (q.w * q.y - q.z * q.x);
		# ~ if (math.fabs(sinp) >= 1):
			# ~ anglespitch = math.copysign(np.pi / 2, sinp);# // use 90 degrees if out of range
		# ~ else:
			# ~ anglespitch = math.asin(sinp);
		
		# ~ #// yaw (z-axis rotation)
		# ~ siny_cosp = +2.0 * (q.w * q.z + q.x * q.y);
		# ~ cosy_cosp = +1.0 - 2.0 * (q.y * q.y + q.z * q.z);  
		# ~ anglesyaw = math.atan2(siny_cosp, cosy_cosp);
		
		
		# ~ print('angles roll = ' +  str(np.rad2deg(anglesroll)))
		# ~ print('angles pitch = ' +  str(np.rad2deg(anglespitch)))
		# ~ print('angles yaw = ' +  str(np.rad2deg(anglesyaw)))
		
		# ~ return anglesroll,anglespitch,anglesyaw
	
	def _generate_filename(self):
		"""Generate the output filename once at initialization."""
		import os
		from datetime import datetime
		
		# Always save relative to the directory where this script is located
		base_dir = os.path.dirname(os.path.abspath(__file__))
		files_dir = os.path.join(base_dir, 'files')

		# Create 'files' folder if it doesn't exist
		if not os.path.exists(files_dir):
			os.makedirs(files_dir)

		# Get participant information from vars
		p_id = getattr(vars, 'participant_id', 'DEFAULT')
		side = getattr(vars, 'side', 'NOSIDE')
		block = getattr(vars, 'block', 'NOBLOCK')
		ttype = getattr(vars, 'training_type', 'NOTYPE')

		# Determine kinematic vs dynamic
		if ttype.lower() == 'angle':
			motion_type = 'Kinematic'
		elif ttype.lower() == 'force':
			motion_type = 'Dynamic'
		else:
			motion_type = 'Unknown'

		# Get current timestamp
		now = datetime.now()
		timestamp = now.strftime("%Y%m%d_%H%M%S")

		# Construct filename with motion type
		return os.path.join(files_dir, f"{p_id}_{side}_{block}_{motion_type}_{timestamp}_juego3.txt")

	def save_incremental(self):
		"""Save only new data since last save (append mode)."""
		try:
			# Determine write mode: 'w' for first save (includes header), 'a' for subsequent
			mode = 'w' if self.last_saved_index == 0 else 'a'

			with open(self.output_filename, mode) as f:
				# Save only new rows since last save
				for i in range(self.last_saved_index, len(self.data_list3)):
					row = self.data_list3[i]
					line = '\t'.join(str(val) for val in row)
					f.write(line + '\n')
			
			# Update the saved index
			self.last_saved_index = len(self.data_list3)
			print(f"💾 Incremental save: {self.last_saved_index} rows saved to {self.output_filename}")
		except Exception as e:
			print(f"Error during incremental save: {e}")
	
	def save_to_csv(self, data):
		"""Final save - only saves remaining unsaved data."""
		try:
			# If there's new data since last incremental save, append it
			if self.last_saved_index < len(data):
				mode = 'w' if self.last_saved_index == 0 else 'a'
				with open(self.output_filename, mode) as f:
					for i in range(self.last_saved_index, len(data)):
						row = data[i]
						line = '\t'.join(str(val) for val in row)
						f.write(line + '\n')
				print(f"✓ Final save complete: {self.output_filename}")
			else:
				print(f"✓ All data already saved: {self.output_filename}")
		except Exception as e:
			print(f"Error saving data to {self.output_filename}: {e}")
		finally:
			if self.soundtrack:
				self.soundtrack.stop()

	def draw_pause_button(self):
		"""Draw the pause/play button in the bottom-right corner."""
		# Button colors
		button_color = (100, 100, 100) if not vars.pause else (50, 150, 50)
		border_color = (200, 200, 200)
		text_color = (255, 255, 255)
		
		# Draw button background
		pygame.draw.rect(vars.screen, button_color, self.button_rect)
		pygame.draw.rect(vars.screen, border_color, self.button_rect, 2)
		
		# Draw button text
		button_font = pygame.font.SysFont('Arial', 18, bold=True)
		if vars.pause:
			text = button_font.render("PLAY ▶", True, text_color)
		else:
			text = button_font.render("PAUSE II", True, text_color)
		
		# Center text on button
		text_rect = text.get_rect(center=self.button_rect.center)
		vars.screen.blit(text, text_rect)

	def draw_menu_button(self):
		"""Draw the menu button in the bottom-right area (left of pause button)."""
		# Button colors
		button_color = (80, 80, 120)
		border_color = (200, 200, 200)
		text_color = (255, 255, 255)
		
		# Draw button background
		pygame.draw.rect(vars.screen, button_color, self.menu_button_rect)
		pygame.draw.rect(vars.screen, border_color, self.menu_button_rect, 2)
		
		# Draw button text
		button_font = pygame.font.SysFont('Arial', 16, bold=True)
		text = button_font.render("MENU", True, text_color)
		
		# Center text on button
		text_rect = text.get_rect(center=self.menu_button_rect.center)
		vars.screen.blit(text, text_rect)

	def main(self):
		"""Main game logic loop for Juego 3."""
		if self.contador >= self.effective_trials:
			self.save_to_csv(self.data_list3)
			vars.pause = False
			vars.gameinit = False
			vars.gameScreen = 'menu'
			return
		if not vars.pause and self.pause_start_time is not None:
			self.pause_start_time = None

		# Fill background
		vars.screen.fill(self.BGCOLOR)
		
		# Draw instructions
		vars.screen.blit(self.instructionsSurf, self.instructionsRect)
		self.frame_index += 1
		
		# Update game parameters
		vars.AMPLITUDE= self.amp[self.contador]
		vars.AMPLITUDE2= self.amp2[self.contador]
		self.kpc = self.kp[self.contador]
		vars.step = self.vel[self.contador]
		self.AMPLITUDE = vars.AMPLITUDE
		self.AMPLITUDE2 = 150
		self.xPos2 = 400
		
		# Draw borders
		pygame.draw.rect(vars.screen, self.RED, (self.WIN_CENTERX-350,self.WIN_CENTERY+self.AMPLITUDE2,700 ,1))
		pygame.draw.rect(vars.screen, self.RED, (self.WIN_CENTERX-350,self.WIN_CENTERY-self.AMPLITUDE2,700 ,1))





		if not vars.pause:

			if vars.eje == 0:
				vars.y1b= vars.x1
			elif vars.eje == 1:	
				vars.y1b= vars.y1
			elif vars.eje == 2:	
				vars.y1b= (vars.z1)# -180,  PB 27 12 19
			elif vars.eje > 2:
				vars.eje = 0
				# ~ print(vars.y1b)	
				# ~ vars.y1b= vars.z1	
				
			val50 = (vars.valup+vars.valdo)/2.0
			
			
			#####SHOW OR NOT
			if self.kpc:
				vars.showSquare = True
				self.showSquare2 = False
			else:
				if vars.time - self.inittime2 < 1500:
					vars.showSquare = False
					self.showSquare2 = False
				
				else:
					vars.showSquare = True
					self.showSquare2 = True
				
				
			if val50 == 0:
				vars.font2 = pygame.font.SysFont('Arial', 50)
				vars.screen.fill((255,255,255))
				vars.screen.blit(vars.font2.render("calibrar primero", True, (0,0,0)), (100, 100))
				val50 = 0.001
				vars.gameinit = False
				
				vars.gameScreen = 'menu'					
				
				# ~ elif val50 > 0:
					# ~ vars.y1b = vars.y1b-val50
				# ~ elif val50 < 0:
					# ~ vars.y1b = vars.y1b+val50						
			vars.y1b = vars.y1b-val50
			ran = abs((vars.valup -val50))

			
			
			# ~ pygame.draw.rect(vars.screen, self.BLUE, (self.WIN_CENTERX-50, int(yPos) + self.WIN_CENTERY-10,100 ,20), 2)
			# ~ pygame.draw.rect(vars.screen, self.RED, (self.WIN_CENTERX-50,self.WIN_CENTERY,100 ,1))

				

			vars.factor = 1#0.75	
			# ~ if vars.y1b > -500 and vars.y1b < 500:##PB 27 12 19
			val = vars.y1b
			# ~ val = (self.AMPLITUDE/abs((vars.valup -val50)*vars.factor))*vars.y1b
			val = ((self.AMPLITUDE2*vars.factor)/abs(vars.valup -val50))*vars.y1b

			self.yPosSquare = int(val) + vars.offset
			
			if self.frame_index % self.trail_stride == 0:
				self.posRecord['square'].append((int(self.WIN_CENTERX),  self.WIN_CENTERY - int(self.yPosSquare) ))
			if len(self.posRecord['square']) > self.trail_max:
				del self.posRecord['square'][:-self.trail_max]
			

			
			valme = ((self.AMPLITUDE2*vars.factor)/abs(vars.valup -val50))*(vars.valme-val50)
			ce=self.WIN_CENTERY-int(valme)
			up=self.WIN_CENTERY-self.AMPLITUDE2
			do=self.WIN_CENTERY+self.AMPLITUDE2
			yPosup = ((ce-up)*(self.AMPLITUDE/100))
			yPosdo = ((do-ce)*(self.AMPLITUDE/100))
			# ~ print(yPosup)
			# ~ print(yPosdo)
			if vars.AMPLITUDE == 0:
				pygame.draw.rect(vars.screen, self.BLUE, (self.WIN_CENTERX-50, self.WIN_CENTERY - int(valme) -10,100 ,20), 2)
				yPos2 = self.WIN_CENTERY - int(valme)
				# ~ pygame.draw.rect(vars.screen, self.RED, (self.WIN_CENTERX-50,self.WIN_CENTERY,100 ,1)) 
			if vars.AMPLITUDE >0:
				pygame.draw.rect(vars.screen, self.BLUE, (self.WIN_CENTERX-50, self.WIN_CENTERY-int(abs(yPosup)) -int(valme) -10,100 ,20), 2)
				yPos2 = self.WIN_CENTERY-int(abs(yPosup)) -int(valme)
			if vars.AMPLITUDE <0:
				pygame.draw.rect(vars.screen, self.BLUE, (self.WIN_CENTERX-50, self.WIN_CENTERY+int(abs(yPosdo)) -int(valme) -10,100 ,20), 2)
				yPos2 = self.WIN_CENTERY+int(abs(yPosdo)) -int(valme)
				# ~ pygame.draw.rect(vars.screen, self.RED, (self.WIN_CENTERX-50,self.WIN_CENTERY,100 ,1))
			# ~ print(valme)
			pygame.draw.rect(vars.screen, self.RED, (self.WIN_CENTERX-350,self.WIN_CENTERY-int(valme),700 ,1))
			# ~ self.yback = self.yPosSquare

			# ~ else:
				# ~ self.yPosSquare = self.yback

			ysin = yPos2
			yimu = self.WIN_CENTERY  - int(self.yPosSquare)
			# ~ print(yimu)
			# ~ print(vars.time - self.inittime2)
			# draw the sine ball and label
			if vars.showSquare:
			# draw the sine ball and label
				pygame.draw.circle(vars.screen, self.BLUE, (int(self.WIN_CENTERX),  self.WIN_CENTERY-int(self.yPosSquare) ), 10)
				if self.showSquare2:
					for x, y in self.posRecord['square'][::self.trail_stride]:
						pygame.draw.circle(vars.screen, self.LBLUE, (x, y), 4)
			
			# ~ pygame.draw.circle(vars.screen, self.BLUE, (int(self.xPos2),yimu), 10)   #PB NOV 2024+

			if vars.time - self.inittime2 > 2000:
				self.inittime2 = vars.time
				# ~ if int(self.step/(2*math.pi)) >self.contador+self.contadorb:
				# ~     self.count = 1
				# ~     if self.count-self.count2 == 1:
				self.contador += 1
				self.block_trial += 1
				print(self.contador)
				self.posRecord['square'] = []
				# ~ self.count2 = 1
				if self.contador >= self.effective_trials:
					self.save_to_csv(self.data_list3)
					vars.pause = False
					vars.gameinit = False
					vars.gameScreen = 'menu'
					return
				if self.block_trial >= 40 and self.contador < self.effective_trials:
					self.blocktimes.append((vars.time - self.inittime) / 1000)
					self.data_list3.append(["Pausa_juego3", vars.gameLevel, str(vars.AMPLITUDE), str(vars.step), (str(vars.time - self.inittime2)), (str(self.xPos2)), (str(ysin)), (str(yimu)), (str(yimu - ysin)), (str(-1)), (str(int(self.kp[self.contador-1]))), (str(vars.x1)), (str(vars.y1)), (str(vars.z1))])
					
					# INCREMENTAL SAVE: Save data at pause block for safety
					self.save_incremental()
					
					# ~ vars.f3.write("Pausa_juego3" + '\t'+ vars.gameLevel +'\t'+ str(vars.AMPLITUDE)  +'\t'+  str(vars.step) +'\t'+(str(vars.time - self.inittime2))+'\t'+(str(self.xPos2))+'\t'+(str(ysin)) + '\t'+(str(yimu))+'\t'+(str(yimu-ysin))+'\t'+(str(self.contador))+'\t'+(str(vars.x1))+'\t'+(str(vars.y1))+'\t'+(str(vars.z1))+'\n') ##PB 27 12 19
					print(str(self.contador) + " repeticiones")
					print(str((vars.time - self.inittime) / 1000) + " segundos")
					self.pause_start_time = time()
					vars.pause = True
					self.block_trial = 0
		
				
			# ~ else:
				# ~ self.count = 0
				# ~ self.count2 = 0
			if self.frame_index % self.log_stride == 0:
				kp_index = min(self.contador, self.total_trials - 1)
				self.data_list3.append(["juego3" , vars.gameLevel , str(vars.AMPLITUDE)  ,  str(vars.step) ,(str(vars.time- self.inittime2)),(str(self.xPos2)),(str(ysin)) ,(str(yimu)),(str(yimu-ysin)),(str(self.contador)),(str(int(self.kp[kp_index]))),(str(vars.x1)),(str(vars.y1)),(str(vars.z1))])

			# ~ vars.f3.write("juego3" +'\t'+ vars.gameLevel +'\t'+ str(vars.AMPLITUDE)  +'\t'+  str(vars.step) +'\t'+(str(vars.time - self.inittime2))+'\t'+(str(self.xPos2))+'\t'+(str(ysin)) + '\t'+(str(yimu))+'\t'+(str(yimu-ysin))+'\t'+(str(self.contador))+'\t'+(str(vars.x1))+'\t'+(str(vars.y1))+'\t'+(str(vars.z1))+'\n') ##PB 27 12 19

			
		else:
			print("tiempo "+str(((vars.time-self.inittime)/1000)-self.blocktimes[-1]))
			print("tiempo ejecutado " + str(self.blocktimes[-1]-self.blocktimes[-0]))
			vars.font2 = pygame.font.SysFont('Arial', 50)
			if self.pause_start_time is None:
				self.pause_start_time = time()
			elapsed_time = time() - self.pause_start_time
			remaining_time = max(0, self.PAUSE_DURATION - elapsed_time)
			vars.screen.blit(vars.font2.render("THIS IS A PAUSE", True, (0,0,0)), (100, 100))
			vars.screen.blit(vars.font2.render("THANKS A LOT", True, (0,0,0)), (100, 220))
			vars.screen.blit(vars.font2.render(f"RESUMING IN: {int(remaining_time)} seconds", True, (0,0,0)), (100, 340))

			if elapsed_time >= self.PAUSE_DURATION:
				self.pause_start_time = None
				vars.pause = False
		
		# Draw pause/play button at the end
		self.draw_pause_button()
		
		# Draw menu button
		self.draw_menu_button()
			

