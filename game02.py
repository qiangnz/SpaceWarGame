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
pygame.display.set_caption("My First Game")
clock=pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((50,40))
        self.image.fill(GREEN)
        self.rect=self.image.get_rect()
        #self.rect.x=200
        #self.rect.y=200
        self.rect.center=(WIDTH/2,HEIGHT/2)
    
    def update(self):
        self.rect.x += 2
        if self.rect.left>WIDTH:
            self.rect.right=0

all_sprites=pygame.sprite.Group()
player=Player()
all_sprites.add(player)


# Game Loop
running=True
while running:
    clock.tick(FPS)
    # Get Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    # Update Game
    all_sprites.update()

    # Game Display
    screen.fill((RED))
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()