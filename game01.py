import pygame

FPS=60
WIDTH=500
HEIGHT=600

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
YELLOW=(255,255,0)


# Game Init and Create Window
pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock()
running=True

# Game Loop
while running:
    clock.tick(FPS)
    # Get Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    # Update Game

    # Game Display
    screen.fill((RED))
    pygame.display.update()

pygame.quit()