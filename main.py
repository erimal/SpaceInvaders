#
#   Game to learn python
#   Eric Malm   01/04/2020
#   How to spend time with Corona Virus 

import pygame
import random
import math
from pygame import mixer

# initialize the pygame object

pygame.init()

# Screen
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders")
background = pygame.image.load('bg.jpg')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
# Play backgound music
mixer.music.load('background.wav')
mixer.music.play(-1)

#score 
score = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

# game over font
game_over_font = pygame.font.Font('freesansbold.ttf',64)

#Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6


for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load('alien32.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1)
    enemyY_change.append(40)

#bullet
#Ready state u can see the bullet on the seek
#Fire state u can see the bullet firing 

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# game over function
def game_over_text():
    go = game_over_font.render("GAME OVER ", True, (255,255,255))
    screen.blit(go, (200,250))
    
def show_score(x,y):
    sc = font.render("Score: " + str(score), True, (255,255,255))
    screen.blit(sc, (x,y))
    
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10))
    # Bullet sound
    bullet_sound = mixer.Sound('laser.wav')
    bullet_sound.play()

def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    d = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if d < 27:
        return True
    else:
        return False
            
    
# Game loop
running = True
while running:
    #background 
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # key strokes movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:          
                playerX_change = 0
    
    # screen movement of space ship
    playerX += playerX_change
    
    if playerX <=0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # screen movement of enemy
        
    for i in range(num_of_enemies):
    
        # Game over 
        if enemyY[i] > 450:
            for j in range (num_of_enemies):
                enemyY[j] = 2000  # Move enemy out of the screen
            game_over_text()
            break
        #if score == 4:   # if score is 100 then tripple enemies
        #    num_of_enemies = 12
        #    break
            
        # enemy movement     
        enemyX[i] += enemyX_change[i]   
        if enemyX[i] <=0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
            
        # collision when u fire a bullet
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            #Collision sound
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score +=1
            # initialize again the enemy
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)

        
        # Displaye enemy    
        enemy(enemyX[i],enemyY[i],i)
        
    # Movement of bullet
    if bulletY <= 0 :
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    


   # Displaye palyer and enemy    
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()