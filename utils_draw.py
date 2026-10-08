import pygame

BLACK2 = (30, 30, 30)


def draw_labels(screen, text, delta, color_f, size_f, x, y):
    offset = delta
    for t in text:
        font = pygame.font.Font('freesansbold.ttf', size_f)
        label = font.render(t, True, color_f)
        screen.blit(label, (x, y + offset))
        offset += delta
