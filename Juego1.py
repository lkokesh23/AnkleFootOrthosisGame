import sys, pygame, math, os
from collections import deque
from pygame.locals import *
from time import sleep, time
from random import choice
# ADDED: Serial imports
import serial 
import serial.tools.list_ports 
import time # We will explicitly use time.time() for the pause timer

# This path insertion MUST be present for 'import vars' to work
sys.path.insert(0, "lib") 
import vars
import csv


# --- ADDED: PORT DETECTION LOGIC (Copied from integrated_main.py) ---
ports = []
print("Juego1: Searching for Arduino/USB serial ports...")
for i in serial.tools.list_ports.comports():
    port_info = str(i)
    if 'ACM' in port_info or 'usb' in port_info or 'Arduino' in port_info or 'USB' in port_info or 'COM' in port_info:
        ports.append(port_info.split(" ")[0])
        
if not ports:
    print("Juego1: WARNING: No Arduino/USB serial port detected. Using default placeholder.")
    SERIAL_PORT = 'NO_PORT_FOUND' 
else:
    SERIAL_PORT = ports[0]
    print(f"Juego1: Detected Serial Port: {SERIAL_PORT}")
    
BAUD_RATE = 115200 
# --- END PORT DETECTION ---


class gaming1(object):		
	def __init__(self):		
		vars.pause = False
		# --- NEW: Fixed Pause Duration Setup ---
		self.pause_start_time = None # Tracks the Python system time when pause begins (None = not paused yet)
		self.PAUSE_DURATION = 30 # seconds
        # ---------------------------------------
		self.WHITE      = (255, 255, 255)
		self.DARKRED    = (255,   200,   200)
		self.RED        = (255,   0,   0)
		self.BLACK      = (  0,   0,   0)
		self.GREEN      = (  0, 0,   255) ### HERE BLUE
		self.BLUE       = (  200,   200, 255) ### HERE lightBLUE

		self.BGCOLOR = self.WHITE

		# Reads from vars module initialized in main3.py
		self.WINDOWWIDTH = vars.width 
		self.WINDOWHEIGHT = vars.height 
		self.WIN_CENTERX = int(self.WINDOWWIDTH / 2) 
		self.WIN_CENTERY = int(self.WINDOWHEIGHT / 2) 

		# ADDED: Serial connection state
		self.serial_conn = None 
		self.live_value = 0.0
		
		# Attempt serial connection on initialization
		self.connect_serial()

		# Background soundtrack
		self.soundtrack = None
		try:
			sound_path = os.path.join(
				os.path.dirname(__file__),
				"assets",
				"game1",
				"sound",
				"soundtrack.mp3",
			)
			self.soundtrack = pygame.mixer.Sound(sound_path)
			self.soundtrack.set_volume(0.2)
			pygame.mixer.Sound.play(self.soundtrack, loops=-1)
		except Exception as e:
			print(f"Juego1: soundtrack not available ({e})")
		
		#FPS = vars.fpsLimit # frames per second to run at
		self.target_fps = getattr(vars, 'target_fps', 120)
		self._smoothed_dt = 1.0 / self.target_fps
		self.frame_index = 0
		self.trail_stride = 1
		self.trail_max = 1200
		self.log_stride = 2
		self.data_list1 = [["game","difficulty", "amplitude", "velocity", "time","xpos","y_computer","y_human","y_error","trial","kp","x","y","z"]]
		# ~ self.ffs1 = 1

		# NOTE: vars.archivo must be set in main3.py before this runs.
		try:
			with open(vars.archivo) as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')
				line_count = 0
				self.vel = []
				self.amp = []
				self.kp = []
				self.blocktimes =[0]
				for row in csv_reader:
					if line_count == 0:
						print(f'Column names are {", ".join(row)}')
						line_count += 1
					else:
						# print(f'\t{row[0]}  {row[1]} ')
						self.vel.append(float(row[0]))
						self.amp.append(float(row[1]))
						self.kp.append(float(row[2]))
						line_count += 1
		except FileNotFoundError:
			print(f"ERROR: Configuration file '{vars.archivo}' not found. Using default speed/amplitude.")
			self.vel = [0.008]
			self.amp = [80]
			self.kp = [1]
		except Exception as e:
			print(f"Error reading {vars.archivo}: {e}")
			self.vel = [0.008]
			self.amp = [80]
			self.kp = [1]

		extra_vel = float(getattr(vars, 'extravel', 0.0))
		if extra_vel:
			self.vel = [v + extra_vel for v in self.vel]

		self.total_trials = len(self.vel)
		self.pause_trials = set()
		self.pause_resume_trials = set()
		if self.total_trials >= 10:
			self.pause_trials = set(range(10, self.total_trials + 1, 10))
			self.pause_resume_trials = {trial + 1 for trial in self.pause_trials if trial + 1 <= self.total_trials}


		# standard pygame setup code - REMOVED/COMMENTED OUT CONFLICTING LINES
		# ~ pygame.init() 
		# ~ FPSCLOCK = pygame.time.Clock()
		# ~ DISPLAYSURF = vars.screen #pygame.display.set_mode((WINDOWWIDTH, self.WINDOWHEIGHT))
		# ~ pygame.display.set_caption('Trig Waves')
		self.fontObj = pygame.font.Font('freesansbold.ttf', 16)

		# variables that track visibility modes
		# ~ vars.showSine = True
		# ~ self.showSquare = True ### HERE

		# ~ vars.pause = False

		self.xPos = 0
		vars.stepb = 0 # the current input f
		# ~ vars.stepb2 = 0
		self.contador = 0
		self.count = 0
		self.count2 = 0
		self.contadorb = 0
		self.countb = 0
		self.count2b = 0
		self.inittime = vars.time

		vars.AMPLITUDE= self.amp[self.contador]
		vars.step = self.vel[self.contador]
		self.AMPLITUDE = vars.AMPLITUDE

		### HERE 
		self.posRecord = {
			'sin': deque(maxlen=self.trail_max),
			'square': deque(maxlen=self.trail_max),
		} # keeps track of the ball positions for drawing the waves

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
		vars.gameinit=True
		vars.gameinit2 =True
		
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

	def connect_serial(self):
		"""Attempts to establish a serial connection for the game."""
		global SERIAL_PORT, BAUD_RATE
		if SERIAL_PORT == 'NO_PORT_FOUND':
			print("Juego1: WARNING: Cannot connect, no USB port detected.")
			return
		try:
			# We keep the connection open for the duration of the game
			self.serial_conn = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.001)
			sleep(0.05) # Give Arduino time to reset
			self.serial_conn.flushInput() 
			print(f"Juego1: Connected to {SERIAL_PORT} for live control.")
		except serial.SerialException as e:
			print(f"Juego1: ERROR: Failed to connect to {SERIAL_PORT}. ({e})")
			self.serial_conn = None

	def read_serial_data(self):
		"""Reads and processes data from the serial port, storing it in vars.y1."""
		if self.serial_conn and self.serial_conn.is_open:
			try:
				line = self.serial_conn.readline().decode('utf-8').strip()
				if line:
					self.live_value = float(line)
					
					# --- CRUCIAL STEP: Update vars with live data for the game to use ---
					vars.y1 = self.live_value
					vars.x1 = self.live_value 
					vars.z1 = self.live_value
					# -------------------------------------------------------------------
					
			except ValueError:
				pass # Ignore non-numeric lines
			except serial.SerialTimeoutException:
				pass 
			except Exception as e:
				print(f"Juego1 Read Error: {e}. Closing connection.")
				if self.serial_conn:
					self.serial_conn.close()
				self.serial_conn = None

	def disconnect_serial(self):
		"""Explicitly closes the serial connection."""
		if self.serial_conn and self.serial_conn.is_open:
			self.serial_conn.close()
			print("Juego1: Serial connection closed by game.")


	def salir(self):        
		print('Exportando datos...')
		# NOTE: Sensor disconnection logic commented out since sensor module is external
		# for sensor in self.sensores:
		# 	sensor.device.disconnect()
		# 	sleep(1)
		# for sensor in self.sensores:
		# 	sensor.exportarDatos('datos_%f.txt' % time())
		# print('Exportacion exitosa')
		# sys.exit() # Handled by integrated_main.py now

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
		return os.path.join(files_dir, f"{p_id}_{side}_{block}_{motion_type}_{timestamp}_juego1.txt")

	def save_incremental(self):
		"""Save only new data since last save (append mode)."""
		try:
			# Determine write mode: 'w' for first save (includes header), 'a' for subsequent
			mode = 'w' if self.last_saved_index == 0 else 'a'

			with open(self.output_filename, mode) as f:
				# Save only new rows since last save
				for i in range(self.last_saved_index, len(self.data_list1)):
					row = self.data_list1[i]
					line = '\t'.join(str(val) for val in row)
					f.write(line + '\n')
			
			# Update the saved index
			self.last_saved_index = len(self.data_list1)
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
		"""
		The game's main logic step, called once per frame by main3.py's loop.
		It handles drawing, physics update, and state transition.
		"""
		
		# --- ADDED: Read serial data at the start of every frame ---
		self.read_serial_data()
		# ----------------------------------------------------------
		
		# event handling loop for quit events - REMOVED (now in integrated_main.py)
		
		# fill the screen to draw from a blank state
		vars.screen.fill(self.BGCOLOR)

		# draw instructions
		vars.screen.blit(self.instructionsSurf, self.instructionsRect)
		
		# Check for end of blocks
		if self.contador >= self.total_trials:
			# Signal integrated_main.py to exit the game loop and return to menu
			vars.gameinit = False
			vars.gameScreen = 'menu'
			# Draw end message on screen
			vars.font2 = pygame.font.SysFont('Arial', 50)
			vars.screen.fill(self.WHITE)
			vars.screen.blit(vars.font2.render("THIS IS THE END OF THIS BLOCK", True, self.BLACK), (100, 100))
			vars.screen.blit(vars.font2.render("THANKS A LOT", True, self.BLACK), (100, 300))
			return # Exit the frame update

		# Update current game parameters
		vars.AMPLITUDE= self.amp[self.contador]
		vars.step = self.vel[self.contador]
		self.kpc = int(self.kp[self.contador])
		self.AMPLITUDE = vars.AMPLITUDE
		self.AMPLITUDE2 = 150 ##########150 up and down in 100%
		self.xPos2 = 700
		
		# --- Sine wave calculation ---
		val50 = (vars.valup + vars.valdo) / 2.0
		# Safety check for uncalibrated state
		if val50 == 0 or vars.valup == vars.valdo:
			vars.font2 = pygame.font.SysFont('Arial', 50)
			vars.screen.fill(self.WHITE)
			vars.screen.blit(vars.font2.render("calibrar primero", True, self.BLACK), (100, 100))
			vars.gameinit = False
			vars.gameScreen = 'menu'
			return # Exit the frame update

		valme = ((self.AMPLITUDE2*vars.factor)/abs(vars.valup -val50))*(vars.valme-val50)
		ce=self.WIN_CENTERY-int(valme)
		up=self.WIN_CENTERY-self.AMPLITUDE2
		do=self.WIN_CENTERY+self.AMPLITUDE2
		yPosup = abs(ce-up)#*(self.AMPLITUDE/100))
		yPosdo = abs(do-ce)#*(self.AMPLITUDE/100))
		
		if vars.pause:
			yPos = (-1 * math.sin(0) * (self.AMPLITUDE2*(self.AMPLITUDE/100)))+ (ce-self.WIN_CENTERY)-1
			if self.frame_index % self.trail_stride == 0:
				self.posRecord['sin'].append((int(self.xPos), int(yPos) + self.WIN_CENTERY))
		else:
			if vars.stepb < math.pi:
				yPos = (-1 * math.sin(vars.stepb) * (yPosup*(self.AMPLITUDE/100))) + (ce-self.WIN_CENTERY)
			else:
				yPos = (-1 * math.sin(vars.stepb) * (yPosdo*(self.AMPLITUDE/100))) + (ce-self.WIN_CENTERY)
			if self.frame_index % self.trail_stride == 0:
				self.posRecord['sin'].append((int(self.xPos), int(yPos) + self.WIN_CENTERY))
		
		if vars.showSine:
			# draw the sine ball and wave trace
			pygame.draw.circle(vars.screen, self.RED, (int(self.xPos2), int(yPos) + self.WIN_CENTERY), 13)
			for index, (x, y) in enumerate(self.posRecord['sin']):
				if index % self.trail_stride != 0:
					continue
				if self.xPos - x > 500:
					continue
				pygame.draw.circle(vars.screen, self.DARKRED, ((self.xPos2-int(self.xPos)) + x, y), 4)

		# --- IMU/Human wave drawing ---
		if self.frame_index % self.trail_stride == 0:
			self.posRecord['square'].append((int(self.xPos),  self.WIN_CENTERY - int(self.yPosSquare) ))
		
		if vars.showSquare:
			# draw the IMU ball and wave trace
			pygame.draw.circle(vars.screen, self.GREEN, (int(self.xPos2),  self.WIN_CENTERY-int(self.yPosSquare) ), 10)
			for index, (x, y) in enumerate(self.posRecord['square']):
				if index % self.trail_stride != 0:
					continue
				if self.xPos - x > 500:
					continue
				pygame.draw.circle(vars.screen, self.BLUE, ((self.xPos2-int(self.xPos))+x, y), 4)

		# draw the border lines
		pygame.draw.rect(vars.screen, self.RED, (self.WIN_CENTERX-350,self.WIN_CENTERY+self.AMPLITUDE2,700 ,1))
		pygame.draw.rect(vars.screen, self.RED, (self.WIN_CENTERX-350,self.WIN_CENTERY-self.AMPLITUDE2,700 ,1))
		pygame.draw.rect(vars.screen, self.RED, (self.WIN_CENTERX-350,self.WIN_CENTERY-valme,700 ,1)) # Middle line

		# Draw pause/play button
		self.draw_pause_button()
		
		# Draw menu button
		self.draw_menu_button()
		
		# --- Physics and State Update ---
		dt = getattr(vars, 'dt', 1.0 / self.target_fps)
		# Smooth and clamp frame time to avoid sudden speed jumps.
		if dt < 0:
			dt = 0
		max_dt = 1.0 / 30.0
		if dt > max_dt:
			dt = max_dt
		alpha = 0.2
		self._smoothed_dt = (alpha * dt) + ((1.0 - alpha) * self._smoothed_dt)
		frame_scale = self._smoothed_dt * self.target_fps
		self.frame_index += 1

		if not vars.pause:
			self.xPos += 0.5 * frame_scale
			
			# No explicit trail trimming needed; deque maxlen handles it.
			if self.xPos>=0:
				
				vars.stepb += vars.step * frame_scale # Update sine phase
				
				# Determine when to show the human-controlled ball based on kpc and sine phase
				if self.kpc:
					vars.showSquare = True
				else:
					if vars.stepb < (2*math.pi)*0.75:
						vars.showSquare = False
					else:
						vars.showSquare = True
				
				# Update sensor data (vars.x1, vars.y1, vars.z1 are updated by self.read_serial_data())
				if vars.eje == 0:
					vars.y1b= vars.x1
				elif vars.eje == 1:	
					vars.y1b= vars.y1 # <-- NOW USING THE LIVE SERIAL VALUE
				elif vars.eje == 2:	
					vars.y1b= (vars.z1)
				elif vars.eje > 2:
					vars.eje = 0
				
				# Normalize sensor reading
				vars.y1b = vars.y1b-val50
				vars.factor = 1 # Used for scaling
				
				if vars.y1b > -500 and vars.y1b < 500:
					val = ((self.AMPLITUDE2*vars.factor)/abs(vars.valup -val50))*vars.y1b
					self.yPosSquare = int(val) + vars.offset
					self.yback = self.yPosSquare
				else:
					self.yPosSquare = self.yback
				
				
				# Data logging
				ysin = int(yPos)+self.WIN_CENTERY
				yimu = self.WIN_CENTERY  - int(self.yPosSquare)

				if vars.stepb >= (2*math.pi):
					vars.stepb=0
					self.count = 1
					if self.count-self.count2 == 1:
						self.contador += 1 # Trial complete
						print(self.contador) 
						self.count2 = 1
						if self.contador >= self.total_trials:
							vars.gameinit = False
							vars.gameScreen = 'menu'
							return
						
						# Pause block logic
						if self.contador in self.pause_trials and self.contador < self.total_trials:
							self.blocktimes.append((vars.time-self.inittime)/1000)
							self.data_list1.append(["Pausa_juego1",vars.gameLevel,str(vars.AMPLITUDE),str(vars.step) ,(str(vars.time)),(str(self.xPos2)),(str(ysin)),(str(yimu)),(str(yimu-ysin)),(str(-1)),(str(int(self.kp[self.contador-1]))),(str(vars.x1)),(str(vars.y1)),(str(vars.z1))])
							
							# INCREMENTAL SAVE: Save data at each pause block for safety
							self.save_incremental()

							print(str(self.contador)+" repeticiones")
							print(str((vars.time-self.inittime)/1000)+" segundos")
							
							# --- MODIFICATION 1: Record start time using standard Python time ---
							self.pause_start_time = time.time() 
							vars.stepb = 0 # Reset phase for cleaner transition
							vars.pause = True # Enter pause screen
							# ---------------------------------------------------------------------

						if self.contador in self.pause_resume_trials:
							self.inittime = vars.time # Reset timer after pause
				else:
					self.count = 0
					self.count2 = 0
					
				# Append current frame data
				if self.frame_index % self.log_stride == 0:
					kp_index = min(self.contador, self.total_trials - 1)
					self.data_list1.append(["juego1" , vars.gameLevel , str(vars.AMPLITUDE)  ,  str(vars.step) ,(str(vars.time)),(str(self.xPos2)),(str(ysin)) ,(str(yimu)),(str(yimu-ysin)),(str(self.contador)),(str(int(self.kp[kp_index]))),(str(vars.x1)),(str(vars.y1)),(str(vars.z1))])
		# Pause Screen Logic
		else:
			self.xPos += 0.5 * frame_scale
			vars.font2 = pygame.font.SysFont('Arial', 50)
			
			# --- MODIFICATION 2: Calculate countdown and display ---
			# Only calculate elapsed time if pause was properly started
			if self.pause_start_time is not None:
				elapsed_time = time.time() - self.pause_start_time
				remaining_time = max(0, self.PAUSE_DURATION - elapsed_time)
			else:
				elapsed_time = 0
				remaining_time = self.PAUSE_DURATION
            
			if self.contador < len(self.vel):
				vars.screen.blit(vars.font2.render("THIS IS A PAUSE", True, self.BLACK), (100, 100))
				# Display countdown (integer seconds)
				vars.screen.blit(vars.font2.render(f"RESUMING IN: {int(remaining_time)} seconds", True, self.BLACK), (100, 300))
			else:
				# Handled by the check at the top of the function
				pass 
			# --------------------------------------------------------
				
			# No explicit trail trimming needed; deque maxlen handles it.
			
			if self.xPos >= 0:
				# vars.stepb += vars.step # MODIFICATION 3: REMOVED this line to disable sine-cycle based timer

				# Sensor data reading logic (only for display/background)
				if vars.eje == 0:
					vars.y1b= vars.x1 
				elif vars.eje == 1:	
					vars.y1b= vars.y1
				elif vars.eje == 2:	
					vars.y1b= vars.z1
				elif vars.eje > 2:
					vars.eje = 0
				
				# Sensor/Calibration check logic is repeated here, which is fine
				val50 = (vars.valup+vars.valdo)/2.0
				if val50 == 0:
					# Handled by the check at the top of the function
					pass
				
				vars.y1b = vars.y1b-val50
				vars.factor = 1	
				
				if vars.y1b > -500 and vars.y1b < 500:
					val = ((self.AMPLITUDE2*vars.factor)/abs(vars.valup -val50))*vars.y1b
					self.yPosSquare = int(val) + vars.offset
					self.yback = self.yPosSquare
				else:
					self.yPosSquare = self.yback
				
				valme = ((self.AMPLITUDE2*vars.factor)/abs(vars.valup -val50))*(vars.valme-val50)
				pygame.draw.rect(vars.screen, self.RED, (self.WIN_CENTERX-350,self.WIN_CENTERY-valme,700 ,1))
				
				# --- MODIFICATION 4: Exit pause screen after 30 seconds ---
				if elapsed_time >= self.PAUSE_DURATION:
					self.countb = 1
					vars.stepb = 0
					if self.countb-self.count2b == 1:
						self.contadorb += 1
						self.count2b = 1
						# Exit the pause state when duration is complete
						vars.pause = False 
				else:
					self.countb = 0
					self.count2b = 0