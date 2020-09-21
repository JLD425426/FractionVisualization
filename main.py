import pygame

pygame.init()

# define colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)


# define window
screenDimensions = (800, 500)
screen = pygame.display.set_mode(screenDimensions)
pygame.display.set_caption("425 Project")

# define bool to decide when program ends
isProgramRunning = True

# clock controls framerate of program
clock = pygame.time.Clock()
fps = 60

# main loop
while isProgramRunning:
    # main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isProgramRunning = False
    
    # main logic here

    # drawing here
    screen.fill(WHITE) #clear screen to white

    pygame.draw.rect(screen, RED , [55, 200, 100, 70], 0)
    pygame.draw.line(screen,GREEN, [0, 0], [100, 100], 5)
    pygame.draw.ellipse(screen, BLACK, [20, 20, 250, 100], 2)

    #update screen and set framerate
    pygame.display.flip()
    clock.tick(fps)

#end of main loop
pygame.quit()

