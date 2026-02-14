import sys
print(sys.version)

import pygame
from pygame.locals import *

score = 0
speedx = 10
speedy = 10
pygame.init() # initialise pygame
screen = pygame.display.set_mode((1280, 720)) # initialise display
running = True
clock = pygame.time.Clock()

enemy1speedx = 15 # define enemy speeds
enemy1speedy = 10
enemy2speedx = 10
enemy2speedy = 15

positionx = screen.get_width() / 2 -400
positiony = screen.get_height() / 2

mainrect = pygame.draw.rect(screen, (0,0,0), (positionx-20, positiony-20, 40, 40)) # draw rects
enemy1 = pygame.draw.rect(screen, (255,0,0), (positionx+780, positiony-80, 80, 80))
enemy2 = pygame.draw.rect(screen, (255,0,0), (positionx+780, positiony+80, 80, 80))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # stops the loop if the red 'X' is pressed
            running = False
    
    fps = round(clock.get_fps(), 1)

    pygame.display.set_caption(f"FPS: {fps}, SCORE: {score}") # display fps and score on the window title

    enemy1.x += enemy1speedx # enemy movement logic
    enemy1.y += enemy1speedy 
    enemy2.x -= enemy2speedx
    enemy2.y -= enemy2speedy

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: # detects if the 'W' key is pressed
        mainrect.y -= speedy # y axis works opposite to a graph, so -= must be used
    if keys[pygame.K_s]:
        mainrect.y += speedy
    if keys[pygame.K_a]:
        mainrect.x -= speedx # x axis works similar to a graph, so -= must be used again
    if keys[pygame.K_d]:
        mainrect.x += speedx


    screen.fill("white") # clear the screen

    kill = pygame.draw.rect(screen, (0,0,255), (0, 0, 40, screen.get_height())) # creates border that kills the player

    finish = pygame.draw.rect(screen, (0,255,0), (screen.get_width()-40, screen.get_height()/3, 40, screen.get_height()-(screen.get_height()*2)/3)) # creates finish line



    # collision logic
    if mainrect.right >= screen.get_width(): # checks if the edges of the player rect are colliding with the edge of the screen
        mainrect.right = screen.get_width() # prevents the player from going past the edge of the screen
    if mainrect.left <= 0:
        mainrect.left = 0
    if mainrect.bottom >= screen.get_height(): 
        mainrect.bottom = screen.get_height()
    if mainrect.top <= 0:
        mainrect.top = 0
    if mainrect.colliderect(kill): # checks if the player collides with a border or an enemy
        mainrect = pygame.draw.rect(screen, (0,0,0), (positionx-20, positiony-20, 40, 40)) # redraws player when they die / collide with a border or enemy
    if mainrect.colliderect(finish):
        mainrect = pygame.draw.rect(screen, (0,0,0), (positionx-20, positiony-20, 40, 40)) # redraws player and adds a point to the score
        score += 1
    if mainrect.colliderect(enemy1):
        mainrect = pygame.draw.rect(screen, (0,0,0), (positionx-20, positiony-20, 40, 40))
    if mainrect.colliderect(enemy2):
        mainrect = pygame.draw.rect(screen, (0,0,0), (positionx-20, positiony-20, 40, 40))
    if enemy1.left <= 0: # checks if the edges of the enemy rect are colliding with the edge of the screen
        enemy1speedx *= -1 # inverts the enemy speed so they bounce off the walls
    if enemy1.right >= screen.get_width():
        enemy1speedx *= -1
    if enemy1.top <= 0:
        enemy1speedy *= -1
    if enemy1.bottom >= screen.get_height():
        enemy1speedy *= -1
    if enemy2.left <= 0:
        enemy2speedx *= -1
    if enemy2.right >= screen.get_width():
        enemy2speedx *= -1
    if enemy2.top <= 0:
        enemy2speedy *= -1
    if enemy2.bottom >= screen.get_height():
        enemy2speedy *= -1
    if enemy2.colliderect(enemy1): # checks if the enemies collide with each other
        enemy1speedy *= -1 # inverts the enemy speed so they bounce off each other
        enemy1speedx *= -1
        enemy2speedy *= -1
        enemy2speedx *= -1

    pygame.draw.rect(screen, (0,0,0), mainrect) # redraws the player and enemy rects every frame
    pygame.draw.rect(screen, (255,0,0), enemy1)
    pygame.draw.rect(screen, (255,0,0), enemy2)

    pygame.display.flip() # puts the changes on screen

    dt = clock.tick(60) / 1000 # limits fps to 60
    enemy1.x += enemy1speedx * dt