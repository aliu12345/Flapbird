import time
import random
import pygame
from pygame.locals import *

pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((800, 500), 0, 32)

GRAVITY = 0.5
JUMP_VELOCITY = -4
PIPE_SPEED = 3
GAP_SIZE = 150
jump_sound = pygame.mixer.Sound('./sounds/Jump.wav')
score_color = (255, 255, 255)
losing_color = (255, 0, 0)
score = 0

add_score = pygame.mixer.Sound("./sounds/Coin.wav")
score_font = pygame.font.SysFont('Arial', 50)
losing_song = pygame.mixer.Sound("./sounds/Womp Womp Womp sound effect.wav")
bird = pygame.image.load('./images/Flappy-Bird-PNG-File.png')
background = pygame.image.load("./images/background.png")
bird = pygame.transform.scale(bird, (100, 50))
pipe = pygame.image.load('./images/pipe.png')
upside_down_pipe = pygame.image.load("./images/upside_down_pipe.png")
load_final_score_color = (255, 255, 255)
pygame.mixer.music.load('./sounds/flappy_bird_music.wav')
background = pygame.transform.scale(background, (800, 500))
pygame.mixer.music.play(-1)
load_final_score_font = pygame.font.SysFont('Arial', 20)

vine_boom = pygame.mixer.Sound("./sounds/Vine boom sound effect slightly bass boosted.wav")
lose_sound = pygame.mixer.Sound('./sounds/Oops.wav')
game_over = False
x, y = (0, 200)
y_velocity = 0
pipe_x = 800
bird_passed_pipes = False
clock = pygame.time.Clock()
losing_font = pygame.font.SysFont('Arial', 50)
losing_text = losing_font.render('Game Over', True, losing_color)

def losing_screen():
    global game_over
    screen.fill((0, 0, 0))
    pygame.mixer.music.stop()
    screen.blit(losing_text, (265, 200))
    screen.blit(load_final_score_text, (310, 400))
    pygame.display.update()
    lose_sound.play()
    time.sleep(2)
    losing_song.play()
    time.sleep(4)
    game_over = True

def new_pipe_sizes():
    bottom_pipe_height = random.randint(100, 300)
    top_pipe_height = 500 - GAP_SIZE - bottom_pipe_height
    return bottom_pipe_height, top_pipe_height
bottom_pipe_height, top_pipe_height = new_pipe_sizes()
bird_rect = bird.get_rect(topleft=(x, y))
pipe_rect = pipe.get_rect(topleft=(pipe_x, 500 - bottom_pipe_height))
upside_down_pipe_rect = upside_down_pipe.get_rect(topleft=(pipe_x, 0))

while not game_over:
    pipe = pygame.transform.scale(pipe, (100, bottom_pipe_height))
    upside_down_pipe = pygame.transform.scale(upside_down_pipe, (100, top_pipe_height))
    score_text = score_font.render(f'Score: {score}', True, score_color)
    pipe_create = False
    load_final_score_text = load_final_score_font.render(f'Your score was {score}', True, load_final_score_color)
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
        losing_screen()
    if y < 0:
        y = 0
    if x < 0:
        x = 0

    y += y_velocity
    y_velocity += GRAVITY

    pipe_x -= PIPE_SPEED

    if pipe_x < -100:
        pipe_x = 800
        bottom_pipe_height, top_pipe_height = new_pipe_sizes()
        bird_passed_pipes = False
        pipe_create = True

    if pipe_create:
        score += 1

    bird_rect.topleft = (x, y)
    pipe_rect = pipe.get_rect(topleft=(pipe_x, 500 - bottom_pipe_height))
    upside_down_pipe_rect = upside_down_pipe.get_rect(topleft=(pipe_x, 0))
    if not bird_passed_pipes and bird_rect.left > pipe_rect.right:
        add_score.play()
        score += 1
        bird_passed_pipes = True
    if bird_rect.colliderect(pipe_rect) or bird_rect.colliderect(upside_down_pipe_rect):
        losing_screen()
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(score_text, (0, 0))
    screen.blit(bird, bird_rect.topleft)
    screen.blit(upside_down_pipe, (pipe_x, 0))
    screen.blit(pipe, (pipe_x, 500 - bottom_pipe_height))
    pygame.display.update()
    clock.tick(60)
pygame.quit()
