import pygame
import pygame_menu

pygame.init()

# Display dimensions
HEIGHT, WIDTH = 700, 700

# define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = ( 227, 39, 211)


# define displau window
screenDimensions = (HEIGHT, WIDTH)
screen = pygame.display.set_mode(screenDimensions)
pygame.display.set_caption("Main Menu - Fraction Visualization")

def set_difficulty_level(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    # Do the job here !
    pass


# Creating a custom theme based off SOLARIZED
fraction_theme = pygame_menu.themes.THEME_SOLARIZED.copy

# Creating menu screen with theme and message
menu = pygame_menu.Menu(HEIGHT, WIDTH, 'Welcome to Fraction Visualization!',
                       theme=pygame_menu.themes.THEME_SOLARIZED)

# menu = pygame_menu.Menu(300, 400, 'Welcome',
                       # theme=pygame_menu.themes.THEME_BLUE)



menu.add_text_input('Name : ', default='Olive Math')     # Allows for user text input

# Selector allows user to select difficulty
menu.add_selector('Difficulty Level :  ', [('Easy', 1), ('Medium', 2), ('Hard', 3)], onchange=set_difficulty_level)

# Start and quit events
menu.add_button('Start', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

# Loop main menu
menu.mainloop(screen)