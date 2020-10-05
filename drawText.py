import pygame

pygame.font.init()

# Function to create and draw text object
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)