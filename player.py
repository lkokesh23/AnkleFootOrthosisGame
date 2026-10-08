import os
import pygame

ASSETS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "assets", "game2")
)


class Player:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.nave = pygame.image.load(os.path.join(ASSETS_DIR, "nave2.png"))
        self.surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.lives0 = pygame.image.load(os.path.join(ASSETS_DIR, "lives0.png"))
        self.lives1 = pygame.image.load(os.path.join(ASSETS_DIR, "lives1.png"))
        self.lives2 = pygame.image.load(os.path.join(ASSETS_DIR, "lives2.png"))
        self.lives3 = pygame.image.load(os.path.join(ASSETS_DIR, "lives3.png"))
        self.image_lives = [self.lives0, self.lives1, self.lives2, self.lives3]
        self.lives_surface = pygame.Surface((200, 50), pygame.SRCALPHA)
        self.process = pygame.image.load(os.path.join(ASSETS_DIR, "process.png"))
        self.process_surface = pygame.Surface((530, 50), pygame.SRCALPHA)
        self.process_nave = pygame.image.load(os.path.join(ASSETS_DIR, "navedown.png"))
        self.width_pixel = 41
        self.heigth_pixel = 28
        self.lives = 3
        self.soundtrack_error = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "bad.wav"))
        self.reduce_x = 0
        self.reduce_y = 0
        self.lives_pos = (self.screen_width - 230, 20)
        self.process_pos = (self.screen_width - 540, self.screen_height - 60)

    def get_surface(self):
        return self.surface

    def reload(self, x, y):
        self.init_x = x
        self.init_y = y - self.heigth_pixel / 2
        self.surface.fill((255, 255, 255, 0))
        self.surface.blit(self.nave, (0, 0))
        self.screen.blit(self.surface, (self.init_x, self.init_y))
        self.lives_surface.fill((255, 255, 255, 0))
        self.lives_surface.blit(self.image_lives[self.lives], (0, 0))
        self.screen.blit(self.lives_surface, self.lives_pos)
        self.process_surface.fill((255, 255, 255, 0))
        self.process_surface.blit(self.process, (0, 0))
        self.process_surface.blit(self.process_nave, (1, 15))
        self.screen.blit(self.process_surface, self.process_pos)
        self.reduce_x = 0
        self.reduce_y = 0

    def update(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.screen.blit(self.surface, (self.init_x, self.init_y + pos_y))
        self.screen.blit(self.lives_surface, self.lives_pos)
        pos_process = pos_x * (522 - 34) / 3000
        self.process_surface.fill((255, 255, 255, 0))
        self.process_surface.blit(self.process, (0, 0))
        self.process_surface.blit(self.process_nave, (1 + pos_process, 15))
        self.screen.blit(self.process_surface, self.process_pos)

    def reduce_lives(self):
        self.soundtrack_error.set_volume(0.2)
        pygame.mixer.Sound.play(self.soundtrack_error)
        self.lives = max(0, self.lives - 1)
        self.lives_surface.fill((255, 255, 255, 0))
        self.lives_surface.blit(self.image_lives[self.lives], (0, 0))
        self.reduce_x = self.pos_x
        self.reduce_y = self.pos_y

    def get_lives(self):
        return self.lives

    def set_lives(self, lives):
        self.lives = lives
