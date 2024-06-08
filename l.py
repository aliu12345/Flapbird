import time
import random
import pygame
from pygame.locals import *
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((800, 500), 0, 32)

GRAVITY = 0.5
JUMP_VELOCITY = -4
BUILDING_SPEED = 3
jump_sound = pygame.mixer.Sound('./sounds/Jump.wav')
score_color = (255, 255, 255)
losing_color = (255, 0, 0)
score = 0

add_score = pygame.mixer.Sound("./sounds/Coin.wav")
score_font = pygame.font.SysFont('Arial', 50)
losing_song = pygame.mixer.Sound("./sounds/Womp Womp Womp sound effect.wav")
bird = pygame.image.load('./images/Flappy-Bird-PNG-File.png')
background = pygame.image.load("./images/bg.png")
bird = pygame.transform.scale(bird, (100, 50))
building = pygame.image.load('./images/building.png')

building_copy = building.copy()
# https://www.geeksforgeeks.org/pygame-flip-the-image/
upside_down_building = pygame.image.load("./images/upsideDownBuilding.png")

pygame.mixer.music.load('./sounds/BABABOOEY 2.wav')
background = pygame.transform.scale(background, (800, 500))
pygame.mixer.music.play(-1)
vine_boom = pygame.mixer.Sound("./sounds/Vine boom sound effect slightly bass boosted.wav")
game_over = False
x, y = (0, 200)
y_velocity = 0
building_x = 800
lose_sound = pygame.mixer.Sound('./sounds/Oops.wav')
upside_down_building_x = 800
bird_passed_buildings = False
size = (100, random.randint(0, 410))
clock = pygame.time.Clock()
losing_font = pygame.font.SysFont('Arial', 50)
losing_text = losing_font.render('Game Over', True, losing_color)
bird_rect = bird.get_rect(topleft=(x, y))
building_rect = building.get_rect(topleft=(building_x, 300))
upside_down_building_rect = upside_down_building.get_rect(topleft=(upside_down_building_x, 0))
while not game_over:

    building = pygame.transform.scale(building, size)
    upside_down_building = pygame.transform.scale(upside_down_building, (100, 500 - size[1] - 80))
    score_text = score_font.render(f'Score: {score}', True, score_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    pressed = pygame.key.get_pressed()
    if pressed[K_SPACE] or pressed[K_w] or pressed[K_UP]:
        y_velocity = JUMP_VELOCITY
        jump_sound.play()
    if x > (screen.get_width() - bird.get_width()):
        x = screen.get_width() - bird.get_width()
    if y > (screen.get_height() - bird.get_height()):
        game_over = True
    if y < 0:
        y = 0
    if x < 0:
        x = 0


    # https://www.reddit.com/r/pygame/comments/14enzx4/how_to_use_recttopleft/
    bird_rect.topleft = (x, y)
    building_rect.topleft = (building_x, 300)
    upside_down_building_rect.topleft = (upside_down_building_x, 0)
    if building_rect[0] < bird_rect[0] and upside_down_building_rect[0] < bird_rect[0]:
        add_score.play()
        score += 1



    # https://www.pygame.org/docs/ref/rect.html#pygame.Rect.colliderect
    if bird_rect.colliderect(building_rect) or bird_rect.colliderect(upside_down_building_rect):
        screen.fill((0, 0, 0))
        pygame.mixer.music.stop()
        screen.blit(losing_text, (250, 200))
        pygame.display.update()
        lose_sound.play()
        time.sleep(2)
        losing_song.play()
        time.sleep(4)
        game_over = True

    y += y_velocity
    y_velocity += GRAVITY
    upside_down_building_x -= BUILDING_SPEED
    building_x -= BUILDING_SPEED
    if building_x < -building.get_width():
        building_x = 800
        size = (100, random.randint(0, 410))  # Update the building size
        bird_passed_buildings = False

    if upside_down_building_x < -upside_down_building.get_width():
        upside_down_building_x = 800
        bird_passed_buildings = False


    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(score_text, (0, 0))
    screen.blit(bird, (x, y))
    screen.blit(upside_down_building, (upside_down_building_x, 0))
    screen.blit(building, (building_x, 300))
    pygame.display.update()
    clock.tick(60)
pygame.quit()
