import csv
import datetime
import os
import sys
import pygame

sys.path.insert(0, "lib")
import vars

from game2.map import Map
from game2.player import Player
from game2.button import Button
from game2.utils_draw import draw_labels


class gaming2:
    def __init__(self):
        vars.pause = False
        self.completed_trials = 0
        self.total_trials = 1
        self.screen = vars.screen
        self.width = vars.width
        self.height = vars.height
        self.menu_width = int(self.width * 0.28)
        self.game_width = self.width - self.menu_width
        self.state = "enabled"
        self.stage = "Pause"
        self.level = 1
        self.step_x = 1.2
        self.x_pos = 0
        self.result = 0
        self.max_range = getattr(vars, "valup", 100.0)
        self.min_range = getattr(vars, "valdo", 0.0)
        self.map_height = 500
        self.map_y = 0
        self.invert_y = False
        self.vertical_margin = 20
        self.hit_freeze_until = 0
        self.hit_y = 0.0
        self.was_collision = False
        self.data_list2 = [[
            "game",
            "level",
            "time_ms",
            "xpos",
            "y_sensor",
            "lives",
            "result",
            "advance",
            "y1",
            "map_order",
        ]]
        self.output_filename = self._generate_filename()
        self.last_saved_index = 0
        self.frame_index = 0
        self.log_stride = 2
        self.session_start_ticks = pygame.time.get_ticks()
        self.timer_font = pygame.font.SysFont("Arial", 18, bold=True)

        self.button_width = 90
        self.button_height = 40
        self.menu_button_width = 80
        self.menu_button_height = 40
        self.menu_button_x = 10
        self.menu_button_y = self.height - self.menu_button_height - 12
        self.menu_button_rect = pygame.Rect(
            self.menu_button_x, self.menu_button_y, self.menu_button_width, self.menu_button_height
        )
        self.button_x = self.menu_button_x + self.menu_button_width + 10
        self.button_y = self.menu_button_y
        self.button_rect = pygame.Rect(
            self.button_x, self.button_y, self.button_width, self.button_height
        )

        self.assets_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "assets", "game2")
        )
        self.background = pygame.image.load(
            os.path.join(self.assets_dir, "background.png")
        )
        self.background = pygame.transform.scale(self.background, (self.game_width, self.height))
        self.soundtrack = None
        try:
            if not getattr(vars, "audio_disabled", False):
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                self.soundtrack = pygame.mixer.Sound(os.path.join(self.assets_dir, "music.mp3"))
        except Exception as e:
            vars.audio_disabled = True
            print(f"Juego2: soundtrack not available ({e})")

        self.menu_surface = pygame.Surface((self.menu_width, self.height), pygame.SRCALPHA)
        self.menu_surface.fill((250, 250, 250))

        self.map = Map(self.screen)
        self.player = Player(self.screen, self.width, self.height)

        self.init_b = Button(size_f=15, x=20, y=220, width=140, height=36)
        self.restart_b = Button(size_f=15, x=20, y=265, width=140, height=36)
        self.level_b = Button(size_f=15, x=20, y=310, width=140, height=36)
        self.init_menu()
        self.stage = "Start"
        self._load_trial_count()
        if self.soundtrack and not getattr(vars, "audio_disabled", False):
            self.soundtrack.set_volume(0.2)
            pygame.mixer.Sound.play(self.soundtrack, loops=-1)

    def _load_trial_count(self):
        archivo2_path = getattr(vars, "archivo2", None)
        if not archivo2_path or not os.path.exists(archivo2_path):
            for cand in ("pt_rt2.csv", "pt_rt.csv"):
                if os.path.exists(cand):
                    archivo2_path = cand
                    break
            else:
                fallback = getattr(vars, "archivo", None)
                if fallback and os.path.exists(fallback):
                    archivo2_path = fallback
                elif os.path.exists("prepost.csv"):
                    archivo2_path = "prepost.csv"

        total_trials = 0
        if archivo2_path and os.path.exists(archivo2_path):
            try:
                with open(archivo2_path) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=",")
                    for line_count, row in enumerate(csv_reader):
                        if line_count == 0:
                            continue
                        if not row:
                            continue
                        total_trials += 1
            except Exception as e:
                print(f"Juego2: failed to read trials from {archivo2_path}: {e}")

        if total_trials <= 0:
            total_trials = 1

        self.total_trials = total_trials
        if self.total_trials <= 0:
            self.total_trials = 1

    def _generate_filename(self):
        # Always save relative to the directory where this script is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        files_dir = os.path.join(base_dir, "files")

        if not os.path.exists(files_dir):
            os.makedirs(files_dir)

        p_id = getattr(vars, "participant_id", "DEFAULT")
        side = getattr(vars, "side", "NOSIDE")
        block = getattr(vars, "block", "NOBLOCK")
        ttype = getattr(vars, "training_type", "NOTYPE")

        if ttype.lower() == "angle":
            motion_type = "Kinematic"
        elif ttype.lower() == "force":
            motion_type = "Dynamic"
        else:
            motion_type = "Unknown"

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(files_dir, f"{p_id}_{side}_{block}_{motion_type}_{timestamp}_juego2.txt")

    def save_incremental(self):
        try:
            mode = "w" if self.last_saved_index == 0 else "a"
            with open(self.output_filename, mode) as f:
                for i in range(self.last_saved_index, len(self.data_list2)):
                    row = self.data_list2[i]
                    line = "\t".join(str(val) for val in row)
                    f.write(line + "\n")
            self.last_saved_index = len(self.data_list2)
        except Exception as e:
            print(f"Error during incremental save: {e}")

    def save_to_csv(self, data):
        try:
            if self.last_saved_index < len(data):
                mode = "w" if self.last_saved_index == 0 else "a"
                with open(self.output_filename, mode) as f:
                    for i in range(self.last_saved_index, len(data)):
                        row = data[i]
                        line = "\t".join(str(val) for val in row)
                        f.write(line + "\n")
                print(f"OK Final save complete: {self.output_filename}")
            else:
                print(f"OK All data already saved: {self.output_filename}")
        except Exception as e:
            print(f"Error saving data to {self.output_filename}: {e}")
        finally:
            self.stop_soundtrack()

    def stop_soundtrack(self):
        if self.soundtrack:
            self.soundtrack.stop()

    def draw_pause_button(self):
        button_color = (100, 100, 100) if not vars.pause else (50, 150, 50)
        border_color = (200, 200, 200)
        text_color = (255, 255, 255)
        pygame.draw.rect(self.screen, button_color, self.button_rect)
        pygame.draw.rect(self.screen, border_color, self.button_rect, 2)
        button_font = pygame.font.SysFont("Arial", 16, bold=True)
        text = "PLAY" if vars.pause else "PAUSE"
        label = button_font.render(text, True, text_color)
        self.screen.blit(label, label.get_rect(center=self.button_rect.center))

    def draw_menu_button(self):
        button_color = (80, 80, 120)
        border_color = (200, 200, 200)
        text_color = (255, 255, 255)
        pygame.draw.rect(self.screen, button_color, self.menu_button_rect)
        pygame.draw.rect(self.screen, border_color, self.menu_button_rect, 2)
        button_font = pygame.font.SysFont("Arial", 14, bold=True)
        label = button_font.render("MENU", True, text_color)
        self.screen.blit(label, label.get_rect(center=self.menu_button_rect.center))

    def init_menu(self):
        self.menu_surface.fill((250, 250, 250))
        draw_labels(
            screen=self.menu_surface,
            text=[""],
            delta=0,
            color_f=(30, 30, 30),
            size_f=20,
            x=20,
            y=20,
        )
        draw_labels(
            screen=self.menu_surface,
            text=[
                f"Participant: {getattr(vars, 'participant_id', 'NOID')}",
                f"Side: {getattr(vars, 'side', 'NOSIDE')}",
                f"Block: {getattr(vars, 'block', 'NOBLOCK')}",
                f"Type: {getattr(vars, 'training_type', 'NOTYPE')}",
                f"Level: {self.level}",
            ],
            delta=18,
            color_f=(30, 30, 30),
            size_f=14,
            x=20,
            y=60,
        )
        draw_labels(
            screen=self.menu_surface,
            text=["Result:", f"{self.result}%"],
            delta=18,
            color_f=(30, 30, 30),
            size_f=16,
            x=20,
            y=155,
        )

        if self.stage == "Pause":
            self.init_b.draw(self.menu_surface, "Start", (50, 150, 50), (255, 255, 255))
            self.level_b.draw(self.menu_surface, "Level", (50, 150, 50), (255, 255, 255))
            self.restart_b.draw(self.menu_surface, "Restart", (50, 150, 50), (255, 255, 255))
        elif self.stage == "Start":
            self.init_b.draw(self.menu_surface, "Start", (180, 180, 180), (255, 255, 255))
            self.level_b.draw(self.menu_surface, "Level", (180, 180, 180), (255, 255, 255))
            self.restart_b.draw(self.menu_surface, "Restart", (50, 150, 50), (255, 255, 255))
        else:
            self.init_b.draw(self.menu_surface, "Start", (180, 180, 180), (255, 255, 255))
            self.level_b.draw(self.menu_surface, "Level", (180, 180, 180), (255, 255, 255))
            self.restart_b.draw(self.menu_surface, "Restart", (180, 180, 180), (255, 255, 255))

        self.screen.blit(self.menu_surface, (0, 0))

        pygame.draw.line(self.screen, (41, 155, 229), (0, 3), (self.width, 3), 6)
        pygame.draw.line(
            self.screen, (41, 155, 229), (0, self.height - 3), (self.width, self.height - 3), 6
        )
        pygame.draw.line(self.screen, (41, 155, 229), (3, 0), (3, self.height), 6)
        pygame.draw.line(
            self.screen, (41, 155, 229), (self.width - 3, 0), (self.width - 3, self.height), 6
        )
        pygame.draw.line(
            self.screen,
            (41, 155, 229),
            (self.menu_width - 3, 0),
            (self.menu_width - 3, self.height),
            4,
        )

        self.screen.blit(self.background, (self.menu_width, 0))
        map_x = self.menu_width + 10
        map_y = int(self.height * 0.08)
        self.map_y = map_y
        self.map.reload(map_x, map_y, self.level)
        self.player.reload(map_x + 20, map_y + 190)

    def set_level(self, level):
        self.level = level
        self.step_x = 1.0 + (self.level - 1) * 0.6

    def get_pixel_scale(self, angle):
        min_val = self.min_range
        max_val = self.max_range
        if max_val == min_val:
            return 0
        if not hasattr(self.player, "init_y"):
            return 0

        if min_val > angle:
            angle = min_val
        if max_val < angle:
            angle = max_val

        top_bound = self.map_y + self.vertical_margin
        bottom_bound = self.map_y + self.map_height - self.player.heigth_pixel - self.vertical_margin
        top_offset = top_bound - self.player.init_y
        bottom_offset = bottom_bound - self.player.init_y

        normalized = (angle - min_val) / (max_val - min_val)
        if self.invert_y:
            pixel_value = top_offset + (bottom_offset - top_offset) * normalized
        else:
            pixel_value = bottom_offset + (top_offset - bottom_offset) * normalized
        return pixel_value

    def restart_game(self):
        self.soundtrack.stop()
        self.x_pos = 0
        self.player.set_lives(3)
        self.stage = "Pause"
        self.result = 0
        self.init_menu()
        self.save_incremental()

    def start_next_trial(self):
        self.x_pos = 0
        self.player.set_lives(3)
        self.result = 0
        self.hit_freeze_until = 0
        self.hit_y = 0.0
        self.was_collision = False
        self.stage = "Start"
        self.init_menu()
        if self.soundtrack and not getattr(vars, "audio_disabled", False):
            self.soundtrack.set_volume(0.2)
            pygame.mixer.Sound.play(self.soundtrack, loops=-1)

    def set_end(self):
        self.soundtrack.stop()
        self.stage = "End"
        self.player.set_lives(3)
        self.x_pos = 0
        self.init_menu()
        self.completed_trials += 1
        self.save_incremental()  # Save the data right after losing all 3 lives / ending the level
        if self.completed_trials >= self.total_trials:
            vars.gameScreen = "menu"
            self.state = "disabled"
            return
        self.start_next_trial()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.stage == "End":
                if self.restart_b.is_click(event.pos):
                    self.restart_game()
                return
            if self.stage == "Pause":
                if self.init_b.is_click(event.pos):
                    self.stage = "Start"
                    self.init_menu()
                    if self.soundtrack and not getattr(vars, "audio_disabled", False):
                        self.soundtrack.set_volume(0.2)
                        pygame.mixer.Sound.play(self.soundtrack, loops=-1)
                elif self.level_b.is_click(event.pos):
                    next_level = self.level + 1
                    if next_level > 3:
                        next_level = 1
                    self.set_level(next_level)
                    self.init_menu()
                elif self.restart_b.is_click(event.pos):
                    self.restart_game()
            elif self.stage == "Start":
                if self.restart_b.is_click(event.pos):
                    self.restart_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.stage == "End":
                self.stage = "Pause"
                self.init_menu()

    def update(self):
        self.frame_index += 1
        if self.stage == "Start":
            self.screen.blit(self.background, (self.menu_width, 0))
            y_sensor = self.get_pixel_scale(vars.y1)
            if pygame.time.get_ticks() < self.hit_freeze_until:
                y_sensor = self.hit_y
            self.map.update(self.x_pos)
            self.player.update(self.x_pos, y_sensor)

            collision = False
            if not vars.pause:
                if 3000 + self.step_x > self.x_pos:
                    collision = self.map.collision(self.player)
                    if collision and not self.was_collision:
                        self.hit_freeze_until = pygame.time.get_ticks() + 250
                        self.hit_y = y_sensor
                    self.x_pos += self.step_x
                    if collision and self.player.get_lives() == 0:
                        self.result = int(self.x_pos * 100 / 3000)
                        self.set_end()
                else:
                    self.result = int(self.x_pos * 100 / 3000)
                    self.set_end()
            self.was_collision = collision
        else:
            self.screen.blit(self.background, (self.menu_width, 0))

        self.screen.blit(self.menu_surface, (0, 0))
        self.draw_menu_button()
        self.draw_pause_button()
        elapsed_ms = max(0, pygame.time.get_ticks() - self.session_start_ticks)
        elapsed_min = int(elapsed_ms / 60000)
        timer_text = self.timer_font.render(f"Time: {elapsed_min} min", True, (0, 0, 0))
        self.screen.blit(timer_text, (12, 10))

        if self.frame_index % self.log_stride == 0:
            map_order = getattr(self.map, "last_map_order", [])
            advance = int(self.x_pos * 100 / 3000)
            self.data_list2.append(
                [
                    "juego2",
                    self.level,
                    pygame.time.get_ticks(),
                    round(self.x_pos, 3),
                    round(vars.y1, 3),
                    self.player.get_lives(),
                    self.result,
                    advance,
                    round(vars.y1, 3),
                    "[" + ",".join(str(item) for item in map_order) + "]",
                ]
            )

    def main(self):
        self.update()

    def get_state(self):
        return self.state
