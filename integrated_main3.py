#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#to do,  1. save the %results in game 2, save the map block of game2

import pygame
import sys
import os 
import serial
import serial.tools.list_ports 
import time
import datetime 
from pygame.locals import *

# --- PROJECT IMPORTS ---
try:
    sys.path.insert(0, "lib")
    import vars
except ImportError:
    print("FATAL ERROR: Could not import 'vars' module. Please ensure 'lib/vars.py' exists.")
    sys.exit()

try:
    from Juego1 import gaming1 
except ImportError:
    print("FATAL ERROR: Could not import 'gaming1' from 'Juego1.py'. Please ensure 'Juego1.py' exists.")
    class gaming1:
        def __init__(self): pass
        def main(self): print("Juego1 placeholder main called.")

try:
    import Juego2
except ImportError:
    print("FATAL ERROR: Could not import 'Juego2' module. Please ensure 'Juego2.py' exists.")
    class Juego2:
        class gaming2:
            def __init__(self): pass
            def main(self): print("Juego2 placeholder main called.")
            def get_state(self): return "disabled"

try:
    import Juego3
except ImportError:
    print("FATAL ERROR: Could not import 'Juego3' module. Please ensure 'Juego3.py' exists.")
    class Juego3:
        class gaming1:
            def __init__(self): pass
            def main(self): print("Juego3 placeholder main called.")
# --- END PROJECT IMPORTS ---

# ----------------------------------------------------
# --- SERIAL PORT DETECTION LOGIC & GLOBALS ---
# ----------------------------------------------------
ports = []
print("Searching for Arduino/USB serial ports...")
for i in serial.tools.list_ports.comports():
	port_info = str(i)
	print(f"Found Port: {port_info}")
	if 'ACM' in port_info or 'usb' in port_info or 'Arduino' in port_info or 'USB' in port_info or 'COM' in port_info:
		ports.append(port_info.split(" ")[0])

if not ports:
    print("\nWARNING: No Arduino/USB serial port detected. Using default placeholder.")
    SERIAL_PORT = 'NO_PORT_FOUND' 
else:
    SERIAL_PORT = ports[0]
    print(f"\n--- Detected Serial Port: {SERIAL_PORT} ---\n")

BAUD_RATE = 115200 

# NEW GLOBAL SERIAL CONNECTION OBJECT
global global_serial_conn
global_serial_conn = None
# ----------------------------------------------------

# --- CONSTANTS ---
COLOR_INACTIVE = (100, 100, 100)
COLOR_ACTIVE = (255, 0, 0)
COLOR_BUTTON = (50, 50, 200)
COLOR_BUTTON_HOVER = (100, 100, 255)
COLOR_TEXT = (0, 0, 0)
COLOR_BACKGROUND = (255, 255, 255)
COLOR_CONNECT = (0, 150, 50) 
COLOR_DISCONNECT = (200, 50, 50) 
COLOR_RETURN = (200, 50, 50) 
COLOR_CONNECTED_STATUS = (0, 200, 70)
COLOR_DISCONNECTED_STATUS = (255, 100, 100)
COLOR_SELECTED = (0, 150, 50) 


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# --- PYGAME INITIALIZATION ---
pygame.init()
pygame.display.set_caption("Neuro Rehab Training")
screen = None
font = pygame.font.SysFont('Arial', 25) 
clock = pygame.time.Clock()

global global_quit
global_quit = False 
# ----------------------------------------------------

# ----------------------------------------------------
# --- HELPER FUNCTIONS ---
# ----------------------------------------------------

def load_default_settings(settings_path):
    """Loads key=value settings and applies supported defaults to vars."""
    if not os.path.exists(settings_path):
        print(f"Settings file not found: {settings_path}")
        return

    supported_keys = {
        'participant_id': 'participant_id',
        'side': 'side',
        'block': 'block',
        'training_type': 'training_type',
        'fullscreen': 'fullscreen',
        'extravel': 'extravel',
    }

    try:
        with open(settings_path, 'r') as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                key, value = line.split('=', 1)
                key = key.strip().lower()
                value = value.strip()
                if key not in supported_keys:
                    continue

                if key == 'side':
                    value = value.upper()
                elif key == 'block':
                    value = value.lower()
                elif key == 'training_type':
                    value = value.capitalize()
                elif key == 'fullscreen':
                    value = parse_bool(value)
                elif key == 'extravel':
                    try:
                        value = float(value)
                    except ValueError:
                        value = 0.0

                setattr(vars, supported_keys[key], value)
        print(f"Loaded settings from: {settings_path}")
    except Exception as e:
        print(f"Warning: Failed to load settings ({settings_path}): {e}")

def parse_bool(value):
    """Converts common string/int representations to bool."""
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in ("1", "true", "yes", "y", "on"):
        return True
    if normalized in ("0", "false", "no", "n", "off"):
        return False
    return False

def init_display():
    """Initializes the pygame display, honoring fullscreen settings."""
    global screen
    fullscreen_enabled = getattr(vars, 'fullscreen', False)
    flags = FULLSCREEN if fullscreen_enabled else 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    vars.screen = screen

def toggle_serial_connection():
    """Attempts to establish or close a persistent serial connection."""
    global global_serial_conn
    
    if global_serial_conn and global_serial_conn.is_open:
        print("Closing existing serial connection.")
        try:
            global_serial_conn.close()
            global_serial_conn = None
            print("Serial connection closed.")
        except Exception as e:
            print(f"Error closing serial connection: {e}")
        return

    if SERIAL_PORT == 'NO_PORT_FOUND':
        print("ERROR: No USB port was detected initially.")
        return

    print(f"Connecting to {SERIAL_PORT}...")
    try:
        new_conn = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.001) 
        time.sleep(0.05) # Give Arduino time to reset
        
        new_conn.flushInput() 
        new_conn.flushOutput() 

        global_serial_conn = new_conn
        vars.serial_conn = global_serial_conn # Store in vars for other modules
        print(f"Connected to {SERIAL_PORT}!")
    except serial.SerialException as e:
        print(f"ERROR: Failed to connect {SERIAL_PORT}. ({e})")
        global_serial_conn = None

def read_serial_data_and_update_vars():
    """
    Reads a line of data from the global serial port, expecting two 
    comma-separated float values (e.g., "Angle,Force"), and updates global vars.
    """
    global global_serial_conn
    
    # Initialize/ensure vars exist for the new angle/force values
    # The Arduino data should be: "Angle,Force"
    if not hasattr(vars, 'force_live'): vars.force_live = 0.0
    if not hasattr(vars, 'angle_live'): vars.angle_live = 0.0
    
    if global_serial_conn and global_serial_conn.is_open:
        try:
            lines_read = 0
            # Read up to 5 lines to clear buffer if needed
            while global_serial_conn.in_waiting > 0 and lines_read < 5: 
                line = global_serial_conn.readline().decode('utf-8').strip()
                lines_read += 1
                
                if line:
                    # EXPECTED FORMAT: "value1,value2" -> "Angle,Force"
                    try:
                        value1_str, value2_str = line.split(',')
                        vars.angle_live = float(value1_str.strip()) # First value is Angle
                        vars.force_live = float(value2_str.strip()) # Second value is Force
                        
                    except ValueError:
                        # Handle case where split fails or float conversion fails
                        print(f"Serial Read Error: Invalid data format in line: '{line}'. Expecting 'Angle,Force'.")
                        return "Error: Invalid data format."
                    
            return "Connected. Data streaming."
            
        except serial.SerialTimeoutException:
            return "Connected. Waiting for data..."
        except Exception as e:
            print(f"Serial Read Error: {e}")
            try:
                global_serial_conn.close()
            except:
                pass
            global_serial_conn = None
            return f"Read Error: {e}. Disconnected."
    else:
        if SERIAL_PORT == 'NO_PORT_FOUND':
            return "No USB Port Detected."
        else:
            return "Disconnected."


# ----------------------------------------------------
# --- UI ELEMENT CLASSES (InputBox and Button) ---
# ----------------------------------------------------

class InputBox:
    """A simple textbox for text input."""
    def __init__(self, x, y, w, h, text='', label=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.label = label
        self.txt_surface = font.render(text, True, COLOR_TEXT)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.active = False
                    self.color = COLOR_INACTIVE
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, COLOR_TEXT)
    
    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        label_surface = font.render(self.label, True, COLOR_TEXT)
        screen.blit(label_surface, (self.rect.x, self.rect.y - 25))
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Button:
    """A clickable button."""
    def __init__(self, x, y, w, h, text, color, hover_color, font_obj, action=None, return_value=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action 
        self.return_value = return_value 
        self.color = color
        self.hover_color = hover_color
        self.font_obj = font_obj 
        self.text_surface = self.font_obj.render(text, True, COLOR_BACKGROUND) 

    def draw(self, screen):
        current_color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=5)
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                return self.return_value
        return None

# ----------------------------------------------------
# --- CALIBRATION SCREEN ---
# ----------------------------------------------------

class CalibrationScreen:
    def __init__(self, screen_obj, font_obj, clock_obj):
        
        # Determine which variable we are calibrating based on participant info
        self.calib_type = getattr(vars, 'training_type', 'Angle').capitalize()

        # Load current calibration values based on the last saved generic values
        self.max_val = vars.valup if hasattr(vars, 'valup') else 0.0
        self.rest_val = vars.valme if hasattr(vars, 'valme') else 0.0
        self.min_val = vars.valdo if hasattr(vars, 'valdo') else 0.0
        
        self.status_message = read_serial_data_and_update_vars()
        self.live_value = self.get_live_value() # Initialize live_value by calling the getter

        self.screen = screen_obj
        self.font = font_obj
        self.clock = clock_obj
        self.SCREEN_WIDTH = SCREEN_WIDTH 
        self.SCREEN_HEIGHT = SCREEN_HEIGHT 

        self.init_buttons()
        
    def get_live_value(self):
        """Returns the current live value based on the calibration type."""
        if self.calib_type == 'Force':
            return vars.force_live
        elif self.calib_type == 'Angle':
            return vars.angle_live
        return 0.0

    def set_max(self):
        """Records the current live value as the Max value."""
        self.max_val = self.get_live_value()
        print(f"MAX {self.calib_type} Value Recorded: {self.max_val:.2f}")
        vars.valup = self.max_val

    def set_rest(self):
        """Records the current live value as the Rest value."""
        self.rest_val = self.get_live_value()
        print(f"REST {self.calib_type} Value Recorded: {self.rest_val:.2f}")
        vars.valme = self.rest_val

    def set_min(self):
        """Records the current live value as the Min value."""
        self.min_val = self.get_live_value()
        print(f"MIN {self.calib_type} Value Recorded: {self.min_val:.2f}")
        vars.valdo = self.min_val

    def init_buttons(self):
        """Creates all buttons: calibration and return."""
        button_w, button_h = 180, 60
        y_calib = self.SCREEN_HEIGHT - 120
        x_spacing = (self.SCREEN_WIDTH - 3 * button_w) // 4
        
        x_max = x_spacing
        # CHANGE 3: Simplified button text (1. Get MAX)
        self.max_button = Button(x_max, y_calib, button_w, button_h, "1. Get MAX", COLOR_BUTTON, COLOR_BUTTON_HOVER, self.font, self.set_max)
        
        x_rest = x_max + button_w + x_spacing
        # CHANGE 3: Simplified button text (2. Get REST)
        self.rest_button = Button(x_rest, y_calib, button_w, button_h, "2. Get REST", COLOR_BUTTON, COLOR_BUTTON_HOVER, self.font, self.set_rest)
        
        x_min = x_rest + button_w + x_spacing
        # CHANGE 3: Simplified button text (3. Get MIN)
        self.min_button = Button(x_min, y_calib, button_w, button_h, "3. Get MIN", COLOR_BUTTON, COLOR_BUTTON_HOVER, self.font, self.set_min)

        self.calib_buttons = [self.max_button, self.rest_button, self.min_button]
        
        # CHANGE 3: Increased Return button size (w=200, h=50) and shifted x slightly
        self.return_button = Button(
            x=20, # Adjusted from 50
            y=30, 
            w=210, # Increased from 150
            h=50,  # Increased from 40
            text="Return to Menu", 
            color=COLOR_RETURN, 
            hover_color=(255, 80, 80), 
            font_obj=self.font,
            return_value=True 
        )

        self.all_buttons = self.calib_buttons + [self.return_button]


    def main_loop(self):
        """The main drawing and event loop for the calibration screen."""
        running = True
        last_fps_report = time.time()
        while running:
            dt_ms = clock.tick(120)
            vars.dt = dt_ms / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                    return True 
                
                for button in self.all_buttons:
                    result = button.handle_event(event)
                    if result is not None:
                        if result is True:
                            running = False 

            self.status_message = read_serial_data_and_update_vars()
            self.live_value = self.get_live_value() # Get the current live value for the selected type
            
            # --- CRITICAL FIX: Update vars.y1 with the live calibration value ---
            # This ensures that vars.y1 (the game's primary input) is constantly 
            # updated with the live sensor value selected for calibration.
            vars.y1 = self.live_value
            # ------------------------------------------------------------------
            
            # --- Drawing ---
            self.screen.fill(COLOR_BACKGROUND)
            title_surface = self.font.render(f"{self.calib_type} Sensor Calibration", True, COLOR_TEXT)
            self.screen.blit(title_surface, (self.SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 100))
            
            # Display sensor reading here
            value_label = self.font.render(f"Instantaneous Reading ({self.calib_type}):", True, COLOR_TEXT)
            value_surface = self.font.render(f"{self.live_value:.2f}", True, COLOR_ACTIVE)
            
            self.screen.blit(value_label, (50, 180))
            self.screen.blit(value_surface, (50 + value_label.get_width() + 10, 180))

            recorded_y = 280
            recorded_values = [
                (f"MAX {self.calib_type} (Max Effort): {self.max_val:.2f}", COLOR_ACTIVE if self.max_val != 0.0 else COLOR_TEXT),
                (f"REST {self.calib_type} (No Contact/Home Pos): {self.rest_val:.2f}", COLOR_TEXT),
                (f"MIN {self.calib_type} (Min Effort): {self.min_val:.2f}", COLOR_TEXT)
            ]
            for text, color in recorded_values:
                surface = self.font.render(text, True, color)
                self.screen.blit(surface, (50, recorded_y))
                recorded_y += 50
                
            for button in self.all_buttons:
                button.draw(self.screen)
                
            pygame.display.flip()
            self.clock.tick(120) 
            
        print("Exiting Calibration Screen.")
        
        # Set vars.y1 to the final calibrated REST value for a clean game start
        vars.y1 = self.rest_val 
        
        return True 


# ----------------------------------------------------
# --- SESSION LOGGING FUNCTIONS ---
# ----------------------------------------------------

def initialize_session_log():
    """Creates a session summary log file in the files/ folder."""
    import os
    
    # Get absolute directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    files_dir = os.path.join(base_dir, 'files')

    # Create files folder if it doesn't exist
    if not os.path.exists(files_dir):
        os.makedirs(files_dir)
    
    # Get participant information
    p_id = getattr(vars, 'participant_id', 'DEFAULT')
    side = getattr(vars, 'side', 'R')
    block = getattr(vars, 'block', 'pre')
    ttype = getattr(vars, 'training_type', 'Angle')
    
    # Create session log filename with timestamp
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    session_file_name = f"session_{p_id}_{side}_{block}_{ttype}_{timestamp}.log"
    session_log_path = os.path.join(files_dir, session_file_name)
    
    # Store the log path in vars for access by other functions
    vars.session_log_path = session_log_path
    
    try:
        with open(session_log_path, 'w') as f:
            f.write("=== SESSION LOG ===\n")
            f.write(f"Participant ID: {p_id}\n")
            f.write(f"Side: {side}\n")
            f.write(f"Block: {block}\n")
            f.write(f"Training Type: {ttype}\n")
            f.write(f"Session Start: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n--- CALIBRATION DATA ---\n")
        print(f"✓ Session log created: {session_log_path}")
    except Exception as e:
        print(f"Warning: Could not create session log: {e}")

def log_calibration_values():
    """Logs calibration values [min, rest, max, time] to the session log."""
    session_log_path = getattr(vars, 'session_log_path', None)
    if not session_log_path:
        return
    
    try:
        min_val = getattr(vars, 'valdo', 0.0)
        rest_val = getattr(vars, 'valme', 0.0)
        max_val = getattr(vars, 'valup', 0.0)
        now = datetime.datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        
        with open(session_log_path, 'a') as f:
            f.write(f"Calibration Completed at: {time_str}\n")
            f.write(f"  Min (valdo):  {min_val}\n")
            f.write(f"  Rest (valme): {rest_val}\n")
            f.write(f"  Max (valup):  {max_val}\n")
            f.write("\n--- GAMES RUN ---\n")
        print(f"✓ Calibration logged: min={min_val}, rest={rest_val}, max={max_val}")
    except Exception as e:
        print(f"Warning: Could not log calibration values: {e}")

def log_game_completion(game_name, trials_count):
    """Logs when a game completes with the number of trials."""
    session_log_path = getattr(vars, 'session_log_path', None)
    if not session_log_path:
        return
    
    try:
        now = datetime.datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        
        with open(session_log_path, 'a') as f:
            f.write(f"{game_name} completed at {time_str} ({trials_count} trials)\n")
        print(f"✓ Game logged: {game_name} - {trials_count} trials")
    except Exception as e:
        print(f"Warning: Could not log game completion: {e}")


# ----------------------------------------------------
# --- ACTION FUNCTIONS ---
# ----------------------------------------------------

def run_calibration():
    """Instantiates and runs the CalibrationScreen."""
    global global_quit
    print("Starting Calibration...")
    
    cal_font = pygame.font.SysFont('Arial', 30)

    cal_screen = CalibrationScreen(
        screen_obj=screen,
        font_obj=cal_font,
        clock_obj=clock     
    )
    
    should_return = cal_screen.main_loop() 
    
    if should_return is False:
        global_quit = True
    
    print("Calibration finished. Returning to menu.")
    
    # Log calibration values to session log
    log_calibration_values()

def run_juego1():
    """Instantiates the gaming1 class and runs its main game loop."""
    global global_quit
    print("Starting Juego 1...")
    
    # --- 1. Initialize Global Vars ---
    vars.width = screen.get_width()
    vars.height = screen.get_height()
    vars.screen = screen
    vars.clock = clock
    vars.time = pygame.time.get_ticks() 
    
    vars.gameLevel = "easy" 
    vars.gameinit = True
    vars.gameinit2 = True
    vars.gameScreen = "juego1"
    vars.target_fps = 60
    
    # Safely retrieve participant details
    p_id = getattr(vars, 'participant_id', 'NOID')
    side = getattr(vars, 'side', 'NOSIDE')
    block = getattr(vars, 'block', 'NOBLOCK')
    ttype = getattr(vars, 'training_type', 'NOTYPE')
    
    # --- Dynamic File Name Generation ---
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    # --- NEW LOGIC: Assign vars.archivo based on Block selection ---
    if block.lower() in ('pre', 'post'):
        vars.archivo = 'prepost.csv'
    elif block.lower() == 'training':
        vars.archivo = 'pt_rt.csv'
    else:
        # Fallback for unexpected block value
        vars.archivo = 'default_block_config.csv'
        
    # Construct the unique data configuration file name (vars.archivo2)
    vars.archivo2 = f"{p_id}_{side}_{block}_{ttype}_{timestamp}_config.csv" 
    print(f"Configuration file assigned: {vars.archivo}")
    # ------------------------------------------------
    
    # Initialize/ensure vars exist
    vars.eje = 0 
    vars.valup = vars.valup if hasattr(vars, 'valup') and vars.valup != 0.0 else 100.0   
    vars.valdo = vars.valdo if hasattr(vars, 'valdo') and vars.valdo != 0.0 else 0.0     
    vars.valme = vars.valme if hasattr(vars, 'valme') and vars.valme != 0.0 else 50.0    
    vars.offset = 0      
    vars.factor = 1.0    
    # Initialize x1, y1, z1 using current vars.y1 (which was set by calibration or default)
    vars.x1 = vars.y1 if hasattr(vars, 'y1') else 0.0 
    vars.y1 = vars.y1 if hasattr(vars, 'y1') else 0.0 
    vars.z1 = vars.y1 if hasattr(vars, 'y1') else 0.0 
    vars.y1b = 0.0       
    vars.showSine = True 
    vars.showSquare = True 
    vars.pause = False 

    # Ensure the new live sensor variables exist
    if not hasattr(vars, 'force_live'): vars.force_live = 0.0
    if not hasattr(vars, 'angle_live'): vars.angle_live = 0.0
        
    # --- 2. Instantiate and Run Game ---
    game_instance = None
    try:
        game_instance = gaming1()
        
        running = True
        last_fps_report = time.time()
        while running:
            dt_ms = clock.tick(vars.target_fps)
            vars.dt = dt_ms / 1000.0
            # CRUCIAL: Read serial data continuously
            read_serial_data_and_update_vars() 
            
            # --- LOGIC: Select which live value to use for the game ---
            # The game uses vars.y1 as its primary control input.
            if vars.training_type.lower() == 'angle':
                vars.y1 = vars.angle_live # Use Angle (first value from Arduino stream)
            elif vars.training_type.lower() == 'force':
                vars.y1 = vars.force_live # Use Force (second value from Arduino stream)
            else:
                # Fallback
                vars.y1 = vars.force_live 
            
            # The game often uses x1 and z1 as redundant copies of y1
            vars.x1 = vars.y1
            vars.z1 = vars.y1
            # ------------------------------------------------------------
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    global_quit = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False 
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    vars.pause = not vars.pause
                # Handle mouse clicks on pause/play button or menu button
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if hasattr(game_instance, 'button_rect') and game_instance.button_rect.collidepoint(mouse_pos):
                        vars.pause = not vars.pause
                    if hasattr(game_instance, 'menu_button_rect') and game_instance.menu_button_rect.collidepoint(mouse_pos):
                        if hasattr(game_instance, 'stop_soundtrack'):
                            game_instance.stop_soundtrack()
                        running = False
            
            vars.time = pygame.time.get_ticks()

            if hasattr(game_instance, 'main'):
                game_instance.main()
            
            if vars.gameScreen != "juego1" or not vars.gameinit:
                running = False
                
            pygame.display.flip()
            if time.time() - last_fps_report >= 2.0:
                print(f"Juego1 FPS: {clock.get_fps():.1f} (target {vars.target_fps})")
                last_fps_report = time.time()

    except Exception as e:
        print(f"ERROR: Failed to run Juego 1: {e}")
        
    finally:
        # 3. Clean up
        # Save all collected game data once per game run
        try:
            if game_instance is not None and hasattr(game_instance, 'data_list1'):
                game_instance.save_to_csv(game_instance.data_list1)
                # Log game completion with trial count
                trials = getattr(game_instance, 'contador', 0)
                log_game_completion('Juego 1', trials)
        except Exception as e:
            print(f"Warning: failed to save Juego1 data: {e}")
            
    print("Juego 1 finished. Returning to menu.")

def run_juego2():
    """Instantiates the Juego2 class and runs its main game loop."""
    global global_quit
    print("Starting Juego 2...")

    # --- 1. Initialize Global Vars ---
    vars.width = screen.get_width()
    vars.height = screen.get_height()
    vars.screen = screen
    vars.clock = clock
    vars.time = pygame.time.get_ticks()

    vars.gameLevel = "easy"
    vars.gameinit = True
    vars.gameinit2 = True
    vars.gameScreen = "juego2"

    # Safely retrieve participant details
    p_id = getattr(vars, 'participant_id', 'NOID')
    side = getattr(vars, 'side', 'NOSIDE')
    block = getattr(vars, 'block', 'NOBLOCK')
    ttype = getattr(vars, 'training_type', 'NOTYPE')

    # --- Dynamic File Name Generation ---
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    # --- Assign config files ---
    if block.lower() in ('pre', 'post'):
        vars.archivo = 'prepost.csv'
    elif block.lower() == 'training':
        vars.archivo = 'pt_rt.csv'
    else:
        vars.archivo = 'default_block_config.csv'

    vars.archivo2 = 'pt_rt2.csv'

    # Initialize/ensure vars exist
    vars.eje = 0
    vars.valup = vars.valup if hasattr(vars, 'valup') and vars.valup != 0.0 else 100.0
    vars.valdo = vars.valdo if hasattr(vars, 'valdo') and vars.valdo != 0.0 else 0.0
    vars.valme = vars.valme if hasattr(vars, 'valme') and vars.valme != 0.0 else 50.0
    vars.offset = 0
    vars.factor = 1.0
    vars.x1 = vars.y1 if hasattr(vars, 'y1') else 0.0
    vars.y1 = vars.y1 if hasattr(vars, 'y1') else 0.0
    vars.z1 = vars.y1 if hasattr(vars, 'y1') else 0.0
    vars.y1b = 0.0
    vars.showSine = True
    vars.showSquare = True
    vars.pause = False

    # Ensure the new live sensor variables exist
    if not hasattr(vars, 'force_live'): vars.force_live = 0.0
    if not hasattr(vars, 'angle_live'): vars.angle_live = 0.0

    # --- 2. Instantiate and Run Game ---
    game_instance = None
    try:
        game_instance = Juego2.gaming2()

        running = True
        last_fps_report = time.time()
        while running:
            read_serial_data_and_update_vars()

            if vars.training_type.lower() == 'angle':
                vars.y1 = vars.angle_live
            elif vars.training_type.lower() == 'force':
                vars.y1 = vars.force_live
            else:
                vars.y1 = vars.force_live

            vars.x1 = vars.y1
            vars.z1 = vars.y1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    global_quit = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    vars.pause = not vars.pause
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if hasattr(game_instance, 'button_rect') and game_instance.button_rect.collidepoint(mouse_pos):
                        vars.pause = not vars.pause
                    if hasattr(game_instance, 'menu_button_rect') and game_instance.menu_button_rect.collidepoint(mouse_pos):
                        running = False
                if hasattr(game_instance, 'handle_event'):
                    game_instance.handle_event(event)

            vars.time = pygame.time.get_ticks()

            if hasattr(game_instance, 'main'):
                game_instance.main()

            if hasattr(game_instance, 'get_state') and game_instance.get_state() == "disabled":
                vars.gameScreen = "menu"
                running = False

            if vars.gameScreen != "juego2" or not vars.gameinit:
                running = False

            pygame.display.flip()
            clock.tick(60)
            if time.time() - last_fps_report >= 2.0:
                print(f"Juego2 FPS: {clock.get_fps():.1f}")
                last_fps_report = time.time()

    except Exception as e:
        print(f"ERROR: Failed to run Juego 2: {e}")

    finally:
        try:
            if game_instance is not None and hasattr(game_instance, 'stop_soundtrack'):
                game_instance.stop_soundtrack()
            if game_instance is not None and hasattr(game_instance, 'data_list2'):
                game_instance.save_to_csv(game_instance.data_list2)
                trials = len(game_instance.data_list2) - 1
                log_game_completion('Juego 2', trials)
        except Exception as e:
            print(f"Warning: failed to save Juego2 data: {e}")

    print("Juego 2 finished. Returning to menu.")

def run_juego3():
    """Instantiates the Juego3 class and runs its main game loop."""
    global global_quit
    print("Starting Juego 3...")
    
    # --- 1. Initialize Global Vars ---
    vars.width = screen.get_width()
    vars.height = screen.get_height()
    vars.screen = screen
    vars.clock = clock
    vars.time = pygame.time.get_ticks() 
    
    vars.gameLevel = "easy" 
    vars.gameinit = True
    vars.gameinit2 = True
    vars.gameScreen = "juego3"
    
    # Safely retrieve participant details
    p_id = getattr(vars, 'participant_id', 'NOID')
    side = getattr(vars, 'side', 'NOSIDE')
    block = getattr(vars, 'block', 'NOBLOCK')
    ttype = getattr(vars, 'training_type', 'NOTYPE')
    
    # --- Dynamic File Name Generation ---
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    
    # --- NEW LOGIC: Assign vars.archivo2 based on Block selection for Juego3 ---
    if block.lower() in ('pre', 'post'):
        vars.archivo2 = 'pt_rt2.csv'
    elif block.lower() == 'training':
        vars.archivo2 = 'pt_rt3.csv'
    else:
        # Fallback for unexpected block value
        vars.archivo2 = 'pt_rt2.csv'
    
    print(f"Configuration file assigned for Juego3: {vars.archivo2}")
    # ------------------------------------------------
    
    # Initialize/ensure vars exist
    vars.eje = 0 
    vars.valup = vars.valup if hasattr(vars, 'valup') and vars.valup != 0.0 else 100.0   
    vars.valdo = vars.valdo if hasattr(vars, 'valdo') and vars.valdo != 0.0 else 0.0     
    vars.valme = vars.valme if hasattr(vars, 'valme') and vars.valme != 0.0 else 50.0    
    vars.offset = 0      
    vars.factor = 1.0    
    # Initialize x1, y1, z1 using current vars.y1 (which was set by calibration or default)
    vars.x1 = vars.y1 if hasattr(vars, 'y1') else 0.0 
    vars.y1 = vars.y1 if hasattr(vars, 'y1') else 0.0 
    vars.z1 = vars.y1 if hasattr(vars, 'y1') else 0.0 
    vars.y1b = 0.0       
    vars.showSine = True 
    vars.showSquare = True 
    vars.pause = False 

    # Ensure the new live sensor variables exist
    if not hasattr(vars, 'force_live'): vars.force_live = 0.0
    if not hasattr(vars, 'angle_live'): vars.angle_live = 0.0
        
    # --- 2. Instantiate and Run Game ---
    game_instance = None
    try:
        game_instance = Juego3.gaming1()
        # CRITICAL: Juego3.__init__ sets vars.gameinit=False; reset it to True to run the game loop
        vars.gameinit = True
        
        running = True
        last_fps_report = time.time()
        while running:
            # CRUCIAL: Read serial data continuously
            read_serial_data_and_update_vars() 
            
            # --- LOGIC: Select which live value to use for the game ---
            # The game uses vars.y1 as its primary control input.
            if vars.training_type.lower() == 'angle':
                vars.y1 = vars.angle_live # Use Angle (first value from Arduino stream)
            elif vars.training_type.lower() == 'force':
                vars.y1 = vars.force_live # Use Force (second value from Arduino stream)
            else:
                # Fallback
                vars.y1 = vars.force_live 
            
            # The game often uses x1 and z1 as redundant copies of y1
            vars.x1 = vars.y1
            vars.z1 = vars.y1
            # ------------------------------------------------------------
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    global_quit = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False 
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    vars.pause = not vars.pause
                # Handle mouse clicks on pause/play button or menu button
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if hasattr(game_instance, 'button_rect') and game_instance.button_rect.collidepoint(mouse_pos):
                        vars.pause = not vars.pause
                    if hasattr(game_instance, 'menu_button_rect') and game_instance.menu_button_rect.collidepoint(mouse_pos):
                        running = False
            
            vars.time = pygame.time.get_ticks()

            if hasattr(game_instance, 'main'):
                game_instance.main()
            
            if vars.gameScreen != "juego3" or not vars.gameinit:
                running = False
                
            pygame.display.flip()
            clock.tick(60)
            if time.time() - last_fps_report >= 2.0:
                print(f"Juego3 FPS: {clock.get_fps():.1f}")
                last_fps_report = time.time()

    except Exception as e:
        print(f"ERROR: Failed to run Juego 3: {e}")
        
    finally:
        # 3. Clean up
        # Save all collected game data once per game run
        try:
            if game_instance is not None and hasattr(game_instance, 'data_list3'):
                game_instance.save_to_csv(game_instance.data_list3)
                # Log game completion with trial count
                trials = getattr(game_instance, 'contador', 0)
                log_game_completion('Juego 3', trials)
        except Exception as e:
            print(f"Warning: failed to save Juego3 data: {e}")
            
    print("Juego 3 finished. Returning to menu.")


# ----------------------------------------------------
# --- SCREEN MANAGEMENT ---
# ----------------------------------------------------

def run_participant_info_screen():
    """
    Handles the participant info input screen using a combination of 
    an InputBox for ID and Buttons for Side, Block, and Training Type.
    Returns "menu" to transition to the main menu or "exit".
    """
    
    # --- 1. State Tracking (Initial/Default values) ---
    selection_state = {
        'Side': getattr(vars, 'side', 'R'),
        'Block': 'pre',
        'Type': getattr(vars, 'training_type', 'Angle')
    }

    # Helper function to create button actions
    def create_selection_action(group_name, value):
        def action():
            selection_state[group_name] = value
        return action

    # --- 2. Input Boxes ---
    id_box = InputBox(100, 150, 400, 32, 
                      text=getattr(vars, 'participant_id', ''), 
                      label='1. Participant ID')
    input_boxes = [id_box]
    y_start = 250
    button_spacing = 10
    
    # --- 3. Button Groups Setup ---
    all_buttons = []
    
    # 3.1 SIDE Group (R/L)
    side_label_surf = font.render('2. Side (R or L):', True, COLOR_TEXT)
    x_pos = 100
    for i, val in enumerate(['R', 'L']):
        action = create_selection_action('Side', val)
        button = Button(
            x=x_pos + i * (120 + button_spacing), y=y_start, w=120, h=40, text=val, 
            color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER, font_obj=font, action=action
        )
        all_buttons.append(button)
    y_start += 100

    # 3.2 TYPE Group (Angle/Force)
    type_label_surf = font.render('3. Training Type (Angle or Force):', True, COLOR_TEXT)
    x_pos = 100
    # Angle is first, Force is second
    for i, val in enumerate(['Angle', 'Force']):
        action = create_selection_action('Type', val)
        button = Button(
            x=x_pos + i * (120 + button_spacing), y=y_start, w=120, h=40, text=val, 
            color=COLOR_BUTTON, hover_color=COLOR_BUTTON_HOVER, font_obj=font, action=action
        )
        all_buttons.append(button)
    
    # CHANGE 1: Move Start Button up by reducing spacing after the last button group
    y_start += 70 # Reduced from 100
    
    start_button = Button(
        x=100, y=y_start + 20, w=150, h=50, 
        text='Start', 
        color=COLOR_CONNECT, 
        hover_color=COLOR_CONNECTED_STATUS, 
        font_obj=font,
        return_value=True 
    )


    waiting_for_input = True
    
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global global_quit
                global_quit = True
                return "exit"
            
            # Input Box handling (for Participant ID)
            for box in input_boxes:
                box.handle_event(event)

            # Button handling
            for button in all_buttons:
                button.handle_event(event)
            
            if start_button.handle_event(event) is True: 
                 waiting_for_input = False
        
        screen.fill(COLOR_BACKGROUND)
        
        # Drawing
        title_surface = font.render("Enter Participant Information", True, COLOR_TEXT)
        screen.blit(title_surface, (100, 80))
        
        # Draw Input Box
        for box in input_boxes:
            box.update()
            box.draw(screen)

        # Draw Button Groups and Labels
        screen.blit(side_label_surf, (100, 225))
        screen.blit(type_label_surf, (100, 325))
        
        # Redraw buttons, highlighting the selected one in each group
        for button in all_buttons:
            # Determine which group the button belongs to
            group_val = None
            
            # Logic to find which group the button text belongs to and check its state
            if button.text == selection_state['Side']:
                group_val = selection_state['Side']
            elif button.text.lower() == selection_state['Block'] or button.text.capitalize() == selection_state['Block'].capitalize():
                if button.text.capitalize() == selection_state['Block'].capitalize():
                    group_val = selection_state['Block'].capitalize()
            elif button.text == selection_state['Type']:
                group_val = selection_state['Type']

            
            if button.text == group_val:
                button.color = COLOR_SELECTED
                button.hover_color = COLOR_SELECTED
            else:
                button.color = COLOR_BUTTON
                button.hover_color = COLOR_BUTTON_HOVER

            button.draw(screen)

        start_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    # --- 5. Finalize and Store Results ---
    
    # Store all values in vars module for global access
    vars.participant_id = id_box.text.strip()
    vars.side = selection_state['Side']
    vars.block = selection_state['Block']
    vars.training_type = selection_state['Type']
    
    print("-" * 30)
    print(f"Participant ID: {vars.participant_id}")
    print(f"Side: {vars.side}")
    print(f"Block: {vars.block}")
    print(f"Training Type: {vars.training_type}")
    print("-" * 30)
    
    # Initialize session log after participant info is collected
    initialize_session_log()
    
    return "menu" 

def run_menu_screen():
    """Handles the main menu with Calibrar and Game buttons.
    Returns "menu", "info", or "exit"."""

    def create_button_action(option_name):
        def action():
            global global_quit
            print(f"--- SELECTED OPTION: {option_name} ---")
            # Accept both English and legacy Spanish option names for compatibility
            key = option_name.lower()
            if key in ("calibrate", "calibrar"):
                run_calibration()
            elif key in ("game1", "juego1"):
                run_juego1()
            elif key in ("game3", "juego3"):
                run_juego2()
            elif key in ("game2", "juego2"):
                run_juego3()
            
            if global_quit:
                nonlocal running
                running = False 
        return action

    start_x = 100
    y_pos = 150
    spacing = 150
    button_w = 120
    button_h = 60

    menu_options = [
        ("Calibrate", "Calibrate"),
        ("Waves", "Game1"),
        ("Square", "Game2"),
        ("Spacecraft", "Game3"),
    ]
    menu_buttons = []
    
    for i, option in enumerate(menu_options):
        label, action_key = option
        x_pos = start_x + i * spacing
        action = create_button_action(action_key)
        
        button = Button(
            x=x_pos, 
            y=y_pos, 
            w=button_w, 
            h=button_h, 
            text=label,
            color=COLOR_BUTTON, 
            hover_color=COLOR_BUTTON_HOVER, 
            font_obj=font, 
            action=action
        )
        menu_buttons.append(button)
        
    # --- ADD CONNECT BUTTON TO MAIN MENU ---
    connect_button = Button(
        x=SCREEN_WIDTH - 280, 
        y=SCREEN_HEIGHT - 80, 
        w=250, 
        h=50, 
        text="Connect/Reset USB", 
        color=COLOR_CONNECT, 
        hover_color=(0, 200, 70), 
        font_obj=font,
        action=toggle_serial_connection
    )
    # ---------------------------------------
    
    # CHANGE 2: Increased Change Participant button size (w=280, h=50) and shifted x
    change_participant_button = Button(
        x=SCREEN_WIDTH - 310, # Adjusted from 280 to 310
        y=30, 
        w=280,                # Increased from 250
        h=50,                 # Increased from 40
        text="Change Participant Info", 
        color=COLOR_BUTTON, 
        hover_color=COLOR_BUTTON_HOVER, 
        font_obj=font,
        return_value="info" # Return "info" to go back to info screen
    )
    # ----------------------------------------------------
    
    # --- EXIT PROGRAM BUTTON (Bottom Left) ---
    exit_button = Button(
        x=50, 
        y=SCREEN_HEIGHT - 80, 
        w=150, 
        h=50, 
        text="Exit Program", 
        color=COLOR_DISCONNECT, 
        hover_color=(255, 100, 100), 
        font_obj=font,
        return_value="exit" # Return "exit" to terminate main loop
    )
    # ----------------------------------------------

    all_buttons = menu_buttons + [connect_button, change_participant_button, exit_button]

    running = True
    next_screen = "menu"
    while running:
        # Read serial data continuously to update global status message
        status_message = read_serial_data_and_update_vars() 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global_quit = True
                running = False
                next_screen = "exit"
            
            for button in all_buttons:
                result = button.handle_event(event)
                if result == "info":
                    next_screen = "info"
                    running = False
                elif result == "exit":
                    global_quit = True
                    next_screen = "exit"
                    running = False
                elif result is not None:
                    # Calibration/Game finished, returned to menu
                    pass
        
        screen.fill(COLOR_BACKGROUND)
        
        title_surface = font.render("Select an Option:", True, COLOR_TEXT)
        screen.blit(title_surface, (start_x, 80))

        for button in menu_buttons:
            button.draw(screen)
            
        # Draw new control buttons
        change_participant_button.draw(screen)
        exit_button.draw(screen)

        # Draw Connect button and status
        connect_button.draw(screen)
        status_color = COLOR_CONNECTED_STATUS if "Connected" in status_message else COLOR_DISCONNECTED_STATUS
        status_surface = font.render(f"USB Status: {status_message}", True, status_color)
        screen.blit(status_surface, (SCREEN_WIDTH - 280, SCREEN_HEIGHT - 120))
            
        pygame.display.flip()
        clock.tick(120)
        
    return next_screen


# ----------------------------------------------------
# --- MAIN PROGRAM LOOP ---
# ----------------------------------------------------

if __name__ == '__main__':
    settings_path = os.path.join(os.path.dirname(__file__), 'settings', 'screen1_defaults.txt')
    load_default_settings(settings_path)

    # Initialize vars with necessary attributes before first use
    vars.participant_id = getattr(vars, 'participant_id', 'DEFAULT')
    vars.side = getattr(vars, 'side', 'R')
    vars.block = getattr(vars, 'block', 'pre')
    vars.training_type = getattr(vars, 'training_type', 'Angle') 
    vars.fullscreen = getattr(vars, 'fullscreen', False)
    vars.extravel = getattr(vars, 'extravel', 0.0)
    vars.valup = getattr(vars, 'valup', 100.0)
    vars.valdo = getattr(vars, 'valdo', 0.0)
    vars.valme = getattr(vars, 'valme', 50.0)
    # Initialize the new variables
    vars.force_live = getattr(vars, 'force_live', 0.0)
    vars.angle_live = getattr(vars, 'angle_live', 0.0)
    vars.y1 = getattr(vars, 'y1', 0.0) # Ensure y1 exists
    # Default configuration file for Juego3 when no generated config exists
    vars.archivo2 = getattr(vars, 'archivo2', 'pt_rt2.csv')

    init_display()

    # Auto-connect USB serial at startup (button still works for reset)
    toggle_serial_connection()

    current_screen = "info"
    
    while True:
        if current_screen == "info":
            result = run_participant_info_screen()
            if result == "exit":
                break
            current_screen = result # Should be "menu"
        elif current_screen == "menu":
            result = run_menu_screen()
            if result == "exit":
                break
            current_screen = result # Can be "menu" (if game finished) or "info"
        
        if global_quit:
            break

    pygame.quit()
    sys.exit()