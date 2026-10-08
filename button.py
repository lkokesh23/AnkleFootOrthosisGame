import pygame

BLACK2 = (30, 30, 30)


class Button:
    def __init__(self, size_f, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.rect_b = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font('freesansbold.ttf', size_f)

    def draw(self, screen, text, color_b, color_f):
        pygame.draw.rect(screen, color_b, self.rect)
        pygame.draw.rect(screen, BLACK2, self.rect_b, 1)
        label = self.font.render(text, True, color_f)
        label_w = (self.width - label.get_width()) / 2
        label_h = (self.height - label.get_height()) / 2
        screen.blit(label, (self.x + label_w, self.y + label_h + 2))

    def is_click(self, pos):
        return self.rect.collidepoint(pos)
