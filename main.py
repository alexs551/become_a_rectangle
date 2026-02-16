import pygame
import random

score = 0
speedx = 10
speedy = 10

pygame.init()  # initialise pygame
screen = pygame.display.set_mode((1280, 720))  # initialise display
running = True
clock = pygame.time.Clock()
powerupon = False

enemy1speedx = 20  # define enemy speeds
enemy1speedy = 20
enemy2speedx = 5
enemy2speedy = 10

# use integers for rect positions
positionx = screen.get_width() // 2 - 400
positiony = screen.get_height() // 2

# randomises location of powerup
powerupx = random.randint(0, screen.get_width() - 20)
powerupy = random.randint(0, screen.get_height() - 20)

# create rects (rect objects store position and size, drawing happens later)
mainrect = pygame.Rect(positionx - 20, positiony - 20, 40, 40)
enemy1 = pygame.Rect(positionx + 780, positiony - 80, 80, 80)
enemy2 = pygame.Rect(random.randint(0, screen.get_width()), positiony + 80, 80, 80)
powerup = pygame.Rect(powerupx, powerupy, 20, 20)
obstacle1 = pygame.Rect(screen.get_width() // 2, screen.get_height() // 2, 50, 700)
obstacle2 = pygame.Rect(screen.get_width() // 3, 0, 50, screen.get_height() // 2)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # stops the loop if the red 'X' is pressed
            running = False

    fps = round(clock.get_fps(), 1)
    pygame.display.set_caption(f"FPS: {fps}, SCORE: {score}")  # display fps and score on the window title

    # enemy movement logic
    enemy1.x += enemy1speedx
    enemy1.y += enemy1speedy
    enemy2.x -= enemy2speedx
    enemy2.y -= enemy2speedy

    keys = pygame.key.get_pressed()

    # move in X first
    if keys[pygame.K_a]:
        mainrect.x -= speedx
    if keys[pygame.K_d]:
        mainrect.x += speedx

    # check X collision with obstacles
    if mainrect.colliderect(obstacle1):
        if keys[pygame.K_d]:
            mainrect.right = obstacle1.left
        if keys[pygame.K_a]:
            mainrect.left = obstacle1.right
    if mainrect.colliderect(obstacle2):
        if keys[pygame.K_d]:
            mainrect.right = obstacle2.left
        if keys[pygame.K_a]:
            mainrect.left = obstacle2.right

    # move in Y second
    if keys[pygame.K_w]:
        mainrect.y -= speedy
    if keys[pygame.K_s]:
        mainrect.y += speedy

    # check Y collision with obstacles
    if mainrect.colliderect(obstacle1):
        if keys[pygame.K_s]:
            mainrect.bottom = obstacle1.top
        if keys[pygame.K_w]:
            mainrect.top = obstacle1.bottom
    if mainrect.colliderect(obstacle2):
        if keys[pygame.K_s]:
            mainrect.bottom = obstacle2.top
        if keys[pygame.K_w]:
            mainrect.top = obstacle2.bottom



    screen.fill("white")  # clear the screen every frame to redraw everything cleanly

    kill = pygame.Rect(0, 0, 40, screen.get_height())  # creates border that kills the player
    finish = pygame.Rect(screen.get_width() - 40,
                         screen.get_height() // 3,
                         40,
                         screen.get_height() - (screen.get_height() * 2) // 3)  # creates finish line

    # keeps player inside screen boundaries
    if mainrect.right >= screen.get_width():
        mainrect.right = screen.get_width()
    if mainrect.left <= 0:
        mainrect.left = 0
    if mainrect.bottom >= screen.get_height():
        mainrect.bottom = screen.get_height()
    if mainrect.top <= 0:
        mainrect.top = 0

    # checks if player collides with kill border
    if mainrect.colliderect(kill):
        mainrect.x = positionx - 20
        mainrect.y = positiony - 20

    # checks if player reaches finish line
    if mainrect.colliderect(finish):
        mainrect.x = positionx - 20
        mainrect.y = positiony - 20
        score += 1

        # randomises location of powerup
        powerup.x = random.randint(0, screen.get_width() - 20)
        powerup.y = random.randint(0, screen.get_height() - 20)

        powerupon = False  # resets powerup state

        # resets enemy speeds
        enemy1speedx = 25
        enemy1speedy = 25
        enemy2speedx = 5
        enemy2speedy = 10

    # checks collision with enemies
    if mainrect.colliderect(enemy1) or mainrect.colliderect(enemy2):
        mainrect.x = positionx - 20
        mainrect.y = positiony - 20

    # makes enemies bounce off screen edges
    if enemy1.left <= 0 or enemy1.right >= screen.get_width():
        enemy1speedx *= -1
    if enemy1.top <= 0 or enemy1.bottom >= screen.get_height():
        enemy1speedy *= -1

    if enemy2.left <= 0 or enemy2.right >= screen.get_width():
        enemy2speedx *= -1
    if enemy2.top <= 0 or enemy2.bottom >= screen.get_height():
        enemy2speedy *= -1

    # makes enemies bounce off each other
    if enemy1.colliderect(enemy2):
        enemy1speedx *= -1
        enemy1speedy *= -1
        enemy2speedx *= -1
        enemy2speedy *= -1

    # checks if player collects the powerup
    if mainrect.colliderect(powerup) and not powerupon:
        powerupon = True  # disables powerup after collection

        # halves enemy speed but keeps it as an integer
        enemy1speedx //= 2
        enemy1speedy //= 2
        enemy2speedx //= 2
        enemy2speedy //= 2

        # moves powerup off screen after collection
        powerup.x = -100
        powerup.y = -100

    # smoother obstacle collision logic
    if enemy1.colliderect(obstacle1):
        enemy1speedx *= -1
        enemy1speedy *= -1
    if enemy2.colliderect(obstacle1):
        enemy2speedx *= -1
        enemy2speedy *= -1
    if enemy1.colliderect(obstacle2):
        enemy1speedx *= -1
        enemy1speedy *= -1
    if enemy2.colliderect(obstacle2):
        enemy2speedx *= -1
        enemy2speedy *= -1
    
    # draws all game objects every frame
    pygame.draw.rect(screen, (0, 0, 255), kill)
    pygame.draw.rect(screen, (0, 255, 0), finish)
    pygame.draw.rect(screen, (0, 0, 0), mainrect)
    pygame.draw.rect(screen, (255, 0, 0), enemy1)
    pygame.draw.rect(screen, (255, 0, 0), enemy2)
    pygame.draw.rect(screen, (128, 0, 0), obstacle1)
    pygame.draw.rect(screen, (128, 0, 0), obstacle2)

    # draws the powerup only if it is not currently collected
    if not powerupon:
        pygame.draw.rect(screen, (255, 0, 255), powerup)

    pygame.display.flip()  # puts the updated frame on screen

    dt = clock.tick(60) / 1000  # limits fps to 60

pygame.quit()
