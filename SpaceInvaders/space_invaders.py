import pygame
import random
import math
import time
from pygame import mixer

pygame.init()
mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders!!")
background = pygame.image.load("SpaceInvaders\eackground.png")
playerImage = pygame.image.load("SpaceInvaders\space-invaders image.png")
icon = pygame.image.load("SpaceInvaders\space-invaders icon.png")
missileImage = pygame.image.load("SpaceInvaders\missile.png")
missile = pygame.transform.scale(missileImage, (50, 50))

pygame.display.set_icon(icon)
clock = pygame.time.Clock()

points = 0
distance = 300
game_over = False
num_of_enemies = 6
over_font = pygame.font.Font('freesansbold.ttf', 64)
MyFont = pygame.font.Font('freesansbold.ttf', 32)

playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImage, (x, y))


enemyX = []
enemyX_change = []
enemyImage = []
enemyY = []
for i in range(num_of_enemies):
    enemyImage.append(pygame.image.load("SpaceInvaders\\ufo_enemy_image.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)


def enemy(x, y, j):
    screen.blit(enemyImage[j], (x, y))


missile_state = "ready"
missileY = 480
missileX = 0


def missile_launch(x, y):
    global missile_state
    missile_state = "fired"
    screen.blit(missile, (x + 8, y - 40))


def show_score(x, y):
    score = MyFont.render("Score : " + str(points), True, (255, 255, 255))
    screen.blit(score, (x, y))





RUNNING = True


def main():
    global missileY
    global missile_state
    global RUNNING
    global playerX_change
    global missileX
    global playerX
    global game_over
    global points
    global distance
    mixer.music.load("SpaceInvaders\eackground.wav")
    mixer.music.set_volume(2)
    mixer.music.play(-1)
    while RUNNING:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -6
                if event.key == pygame.K_RIGHT:
                    playerX_change = 6
                if event.key == pygame.K_SPACE:
                    if missile_state == "ready":
                        missileLaunch = mixer.Sound("SpaceInvaders\laser.wav")
                        missileLaunch.play()
                        missileX = playerX
                        missile_launch(missileX, missileY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for k in range(num_of_enemies):

            if enemyX[k] >= 736:
                enemyX[k] = 736
                enemyX_change[k] -= 4
                enemyY[k] += 30
            elif enemyX[k] <= 0:
                enemyX[k] = 0
                enemyX_change[k] = 4
                enemyY[k] += 30

            if enemyY[k] >= 440:
                game_over = True

        if missile_state == "fired":
            missileY -= 20
            missile_launch(missileX, missileY)
            for k in range(num_of_enemies):
                distance = math.sqrt(math.pow((enemyX[k] - missileX), 2) + math.pow((enemyY[k] - missileY), 2))
                if distance <= 27:
                    points += 1
                    missile_state = "ready"
                    missileY = 480
                    explosion = mixer.Sound("SpaceInvaders\explosion.wav")
                    explosion.play()
                    enemyX[k] = random.randint(0, 736)
                    enemyY[k] = random.randint(50, 150)
                    # print("collision :" + str(points))

        if missileY <= 0:
            missileY = 480
            missile_state = "ready"

        if game_over:
            over_text = over_font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(over_text, (200, 250))
            show_score(340, 320)
            for h in range(num_of_enemies):
                enemyY[h] = 1000

        for h in range(num_of_enemies):
            enemyX[h] += enemyX_change[h]

        player(playerX, playerY)
        for h in range(num_of_enemies):
            enemy(enemyX[h], enemyY[h], h)

        if not game_over:
            show_score(20, 20)
        pygame.display.update()
        clock.tick(100)


instructionFont = pygame.font.Font('freesansbold.ttf', 16)
instructionFont2 = pygame.font.Font('freesansbold.ttf', 19)


def InstructionText():
    white = (255, 255, 255)
    name = MyFont.render('SPACE-INVADERS', True, white)  # name is instructions
    screen.blit(name, (270, 40))
    name = instructionFont2.render('INSTRUCTIONS FOR THE GAME', True, white)
    screen.blit(name, (40, 100))
    instruction_enemy = pygame.image.load("SpaceInvaders\\ufo_enemy_image.png")
    screen.blit(instruction_enemy, (250, 140))
    name = instructionFont.render('•This is the enemy UFO:', True, white)
    screen.blit(name, (40, 170))
    screen.blit(playerImage, (250, 220))
    name = instructionFont.render('•This is your Ship:', True, white)
    screen.blit(name, (40, 250))
    name = instructionFont.render('•In this game your objective is to shoot the enemy UFOs', True, white)
    screen.blit(name, (40, 320))
    name = instructionFont.render('•To do this, move your ship with the left and the right arrow keys', True, white)
    screen.blit(name, (40, 390))
    name = instructionFont.render('•Press space bar to launch missiles which destroy the enemy UFOs', True, white)
    screen.blit(name, (40, 460))
    name = instructionFont.render('•Press space bar to start playing', True, white)
    screen.blit(name, (40, 530))


def instructions():
    RUNNING_of_instructions = True
    mixer.music.load("SpaceInvaders\Among Us Theme.mp3")
    mixer.music.set_volume(2)
    mixer.music.play(-1)
    while RUNNING_of_instructions:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING_of_instructions = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    RUNNING_of_instructions = False
                    main()
        InstructionText()
        pygame.display.update()


instructions()
