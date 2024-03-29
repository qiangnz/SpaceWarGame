import pygame
import random
import os

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
pygame.mixer.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("My First Game")
clock=pygame.time.Clock()

# Load Images
background_img=pygame.image.load(os.path.join("img","background.png")).convert()
player_img=pygame.image.load(os.path.join("img","player.png")).convert()
bullet_img=pygame.image.load(os.path.join("img","bullet.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())

# Load Font
font_name=pygame.font.match_font('arial')

def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(font_name, size)
    text_surface=font.render(text,True,WHITE)
    text_rect=text_surface.get_rect()
    text_rect.centerx=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)

def  draw_health(surf,hp,x,y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect=pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect=pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE, outline_rect,2)
    
# Load Sound
shoot_sound=pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
expl_sounds=[
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound","expl1.wav"))]
pygame.mixer.music.load(os.path.join("sound","background.ogg"))
pygame.mixer.music.set_volume(0.2)

def new_rock():
    r=Rock()
    all_sprites.add(r)
    rocks.add(r)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(player_img, (50,38)) 
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx=8
        self.health=100
    
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
    
    def shoot(self):
        bullet=Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori=random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image=self.image_ori.copy() 
        self.rect=self.image.get_rect()
        self.radius=int(self.rect.width *0.85/2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width )
        self.rect.y = random.randrange(-180, -100)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 5)
        self.total_degree=0
        self.rot_degree=random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree%360
        self.image=pygame.transform.rotate(self.image_ori , self.total_degree)
        center=self.rect.center
        self.rect=self.image.get_rect()
        self.rect.center=center 

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width )
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 10)

class Bullet(pygame.sprite.Sprite):
    ## Get Plane's Position self,x,y
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=bullet_img
        self.image.set_colorkey(BLACK )
        self.rect=self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()
            
# Sprites
all_sprites=pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player=Player()
all_sprites.add(player)
for i in range(8):
    new_rock()
score = 0
# -1 play infinity
pygame.mixer.music.play(-1)

# Game Loop
running=True
while running:
    clock.tick(FPS)
    # Get Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update Game
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets , True, True )
    for hit in hits:
        random.choice(expl_sounds).play()
        score += hit.radius
        new_rock()
    
    # Flase = Rock not Kill True = Rock Kill
    hits = pygame.sprite.spritecollide(player, rocks, True,pygame.sprite.collide_circle)
    for hit in hits:
        new_rock()
        player.health -= hit.radius
        if player.health <=0:
            running = False

    # Game Display
    screen.fill(BLACK) 
    screen.blit(background_img , (0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 15)
    pygame.display.update()

pygame.quit() 