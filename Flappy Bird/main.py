import pygame
import random
from pygame import mixer

pygame.init()
mixer.init()

width = 289
height = 512

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird(New)")
pygame.display.set_icon(pygame.image.load("Flappy Bird/icon.ico"))
clock = pygame.time.Clock()

background_day = pygame.image.load("Flappy Bird/background-day.png")
background_night = pygame.image.load("Flappy Bird/background-night.png")
background = [background_day, background_night]

base = pygame.image.load("Flappy Bird/base.png")
default_font = pygame.font.Font('Flappy Bird/COMIC.TTF', 32)

die_sound = mixer.Sound('Flappy Bird/die.wav')
hit_sound = mixer.Sound('Flappy Bird/hit.wav')
point_sound = pygame.mixer.Sound('Flappy Bird/point.wav')
swoosh_sound = pygame.mixer.Sound('Flappy Bird/swoosh.wav')
wing_sound = pygame.mixer.Sound('Flappy Bird/wing.wav')
audios = [die_sound, hit_sound, point_sound, swoosh_sound, wing_sound]
die_audio_played = False

downflap = pygame.image.load("Flappy Bird/downflap.png")
midflap = pygame.image.load("Flappy Bird/midflap.png")
upflap = pygame.image.load("Flappy Bird/upflap.png")
bird = [downflap, midflap, upflap]

pipeDownY = []
pipeUpY = []

pipeX = []

pipeUp = []
pipeDown = []

pipeV_gap = 140
pipeH_gap = 190

pipeUpRect = []
pipeDownRect = []

pipe_velx_dump = 3
pipe_velX = pipe_velx_dump

playerX = width / 5
playerY = height / 5
bird_vel_y_dump = 9
bird_vel_y = bird_vel_y_dump

spacestate = "down"
# The variable spacestate is of no use, therefore it can be omitted.
pipes_no = 30

day = True

collision_state = []
points = 0

collision_counter = []

gameOver = False
pygame.time.set_timer(pygame.USEREVENT, 250)
bird_index = 0


def pipes_initiator():
    global pipeDownY
    global pipeUpY
    global pipeX
    global pipeUp
    global pipeDown
    global pipeUpRect
    global pipeDownRect

    global day

    global collision_state
    global collision_counter

    pipeDownY = []
    pipeUpY = []

    pipeX = []

    pipeUp = []
    pipeDown = []
    for i in range(pipes_no):
        pipeUp.append(pygame.transform.rotate(pygame.image.load("Flappy Bird/pipe-green.png"), 180))
        pipeDown.append(pygame.image.load("Flappy Bird/pipe-green.png"))

        pipeUpY.append(random.randint(-280, -100))
        pipeDownY.append(pipeUpY[i] + 320 + pipeV_gap)

    for i in range(pipes_no):
        if i == 0:
            pipeX.append(random.randint(500, 700))
        else:
            pipeX.append(pipeX[i - 1] + 52 + pipeH_gap)

    pipeUpRect = []
    pipeDownRect = []

    for i in range(pipes_no):
        pipeUpRect.append(pipeUp[i].get_rect(topleft=(pipeX[i], pipeUpY[i])))
        pipeDownRect.append(pipeDown[i].get_rect(topleft=(pipeX[i], pipeDownY[i])))

    collision_state = []
    collision_counter = []

    for i in range(pipes_no):
        collision_state.append(0)
        collision_counter.append(0)


def pipe_rect_updater():
    for i in range(pipes_no):
        pipeUpRect[i] = (pipeUp[i].get_rect(topleft=(pipeX[i], pipeUpY[i])))
        pipeDownRect[i] = (pipeDown[i].get_rect(topleft=(pipeX[i], pipeDownY[i])))


def main_game():
    global bird_vel_y
    global spacestate
    global points
    global collision_state
    global gameOver
    global pipe_velX
    global playerY
    global day
    global bird_index

    global die_audio_played

    black = (0, 0, 0)
    runner = True

    pipes_initiator()

    while runner:
        screen.fill(black)
        bird_rect = bird[0].get_rect(topleft=(playerX, playerY))
        pipe_rect_updater()
        points_calculator()
        for h in range(pipes_no):
            screen.blit(screen, pipeDownRect[h])
            screen.blit(screen, pipeUpRect[h])
        screen.blit(screen, bird_rect)

        screen.blit(background[0], (0, 0))
        pipe_blitter()
        points_blitter()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runner = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not gameOver:
                        # spacestate = "down"
                        jump()
                        audios[4].play()
                        bird_vel_y = bird_vel_y_dump
                    else:
                        gameOver = False
                        points = 0
                        # spacestate = "down"
                        pipe_velX = pipe_velx_dump
                        pipes_initiator()
                        playerY = height / 5
                        bird_vel_y = bird_vel_y_dump
                        die_audio_played = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not gameOver:
                    # spacestate = "down"
                    jump()
                    audios[3].play()
                    bird_vel_y = bird_vel_y_dump
                else:
                    gameOver = False
                    points = 0
                    # spacestate = "down"
                    pipe_velX = pipe_velx_dump
                    pipes_initiator()
                    playerY = height / 5
                    bird_vel_y = bird_vel_y_dump
                    die_audio_played = False

            # if event.type == pygame.KEYUP:
            # if event.type == pygame.K_SPACE:
            # spacestate = "up"

            # elif event.type == pygame.MOUSEBUTTONUP:
            # spacestate = "up"

            if event.type == pygame.USEREVENT:
                bird_index += 1
                if bird_index > 2:
                    bird_index = 0

        # if spacestate == "down":
        if not gameOver:
            jump()

        for h in range(pipes_no):
            if bird_rect.colliderect(pipeUpRect[h]):
                if pipeX[h] + 52 < playerX + 34:
                    if not die_audio_played:
                        audios[1].play()
                        die_audio_played = True
                    collision_state[h] = 1
                    gameOver = True

            elif bird_rect.colliderect(pipeDownRect[h]):
                if pipeX[h] + 52 < playerX + 34:
                    if not die_audio_played:
                        audios[1].play()
                        die_audio_played = True
                    collision_state[h] = 1
                    gameOver = True

        for h in range(pipes_no):
            if pipeX[h] + 52 < playerX + 34:
                collision_counter[h] = 1

        if pipeX[pipes_no - 1] <= 0:
            pipes_initiator()

        if playerY >= 400 or playerY <= 0:
            if not die_audio_played:
                audios[1].play()
                die_audio_played = True
            gameOver = True

        screen.blit(base, (0, 410))
        pygame.display.update()
        clock.tick(60)


def pipe_blitter():
    global pipe_velX

    for h in range(pipes_no):
        screen.blit(pipeUp[h], (pipeX[h], pipeUpY[h]))
        screen.blit(pipeDown[h], (pipeX[h], pipeDownY[h]))
        pipeX[h] -= pipe_velX


def jump():
    global bird_vel_y
    global playerY

    bird_vel_y -= 0.5
    playerY -= bird_vel_y
    screen.blit(bird[bird_index], (playerX, playerY))


def points_calculator():
    global points
    for j in range(pipes_no):
        if collision_counter[j] == 1:
            if collision_state[j] == 0:
                points += 1
                audios[2].play()
                collision_state[j] = 1


def points_blitter():
    global pipe_velX
    if gameOver:
        text = default_font.render("Game over!!", True, (0, 0, 0))
        screen.blit(text, (width / 5, height / 5))
        text = default_font.render("Your Score: " + str(points), True, (0, 0, 0))
        screen.blit(text, (width / 8, height / 3))
        text = default_font.render("Press SpaceBar to", True, (0, 0, 0))
        screen.blit(text, (width / 23, height / 3 + 70))
        text = default_font.render("play again", True, (0, 0, 0))
        screen.blit(text, (width / 4, height / 2.2 + 70))
        pipe_velX = 0

    else:
        score = default_font.render(str(points), True, (0, 0, 0))
        screen.blit(score, (10, 10))


if __name__ == '__main__':
    main_game()
