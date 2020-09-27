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
    # Do something here
    pass

def start_the_game():
    # Do something here
    pass

def tutorial():
    # Do something here
    pass



# Creating a custom theme based off SOLARIZED
# copy = pygame_menu.themes.THEME_SOLARIZED.copy

# Creating a custom theme from scratch
fraction_theme = pygame_menu.themes.Theme(background_color=(0, 0, 0, 0), # transparent background
                title_shadow=True,
                title_background_color=GREEN
                )

# Adding image to be used as background
myimage = pygame_menu.baseimage.BaseImage(
    image_path="geom_background1.jpg",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
)

# Making the image the background of the theme
fraction_theme.background_color = myimage

# Making underlined title bar
fraction_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE

# Editing font and shadow on title bar
fraction_theme.title_font_color = BLACK
fraction_theme.title_shadow = False

# Creating menu screen with theme and message
menu = pygame_menu.Menu(HEIGHT, WIDTH, 'Welcome to Fraction Visualization!',
                       theme=fraction_theme)

# Setting color for selection box
fraction_theme.selection_color = BLACK

 # Allows for user text input
menu.add_text_input('Name : ', default='Olive Math')

# Selector allows user to select difficulty
menu.add_selector('Difficulty Level :  ', [('Easy', 1), ('Medium', 2), ('Hard', 3)], onchange=set_difficulty_level)

# Start and quit events
menu.add_button('Tutorial', tutorial)
menu.add_button('Start', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

# Loop main menu
menu.mainloop(screen)