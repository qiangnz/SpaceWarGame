import pygame
import random

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
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx=8
    
    def update(self):
        key_pressed=pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx    

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left=0

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((30,40))
        self.image.fill(RED)
        self.rect=self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width )
        self.rect.y = random.randrange(-100, -40)
        # self.speedy=2
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
    
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width )
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

all_sprites=pygame.sprite.Group()
player=Player()
all_sprites.add(player)
# rock=Rock()
# all_sprites.add(rock)

for i in range(8):
    r=Rock()
    all_sprites.add(r)

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
    screen.fill((WHITE))
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()