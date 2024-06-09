import time
import random
import pygame
from pygame.locals import *

pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((800, 500), 0, 32)

# Constants
GRAVITY = 0.5
JUMP_VELOCITY = -4
BUILDING_SPEED = 3
GAP_SIZE = 150  # Space between the buildings for the bird to fly through

# Load assets
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
upside_down_building = pygame.image.load("./images/upsideDownBuilding.png")
coin = pygame.image.load('./images/lightning bolt.png')
pygame.mixer.music.load('./sounds/BABABOOEY 2.wav')
background = pygame.transform.scale(background, (800, 500))
pygame.mixer.music.play(-1)
vine_boom = pygame.mixer.Sound("./sounds/Vine boom sound effect slightly bass boosted.wav")
lose_sound = pygame.mixer.Sound('./sounds/Oops.wav')

# Game variables
game_over = False
x, y = (0, 200)
y_velocity = 0
building_x = 800
coin_x = 800
coin_y = -100
upside_down_building_x = 800
bird_passed_buildings = False
clock = pygame.time.Clock()
losing_font = pygame.font.SysFont('Arial', 50)
losing_text = losing_font.render('Game Over', True, losing_color)
superMode = False
superScore = 0


# Function to generate new building sizes and positions
def new_building_sizes():
    bottom_building_height = random.randint(100, 300)
    top_building_height = 500 - GAP_SIZE - bottom_building_height
    return bottom_building_height, top_building_height


bottom_building_height, top_building_height = new_building_sizes()

# Initial rects
bird_rect = bird.get_rect(topleft=(x, y))
building_rect = building.get_rect(topleft=(building_x, 500 - bottom_building_height))
upside_down_building_rect = upside_down_building.get_rect(topleft=(upside_down_building_x, 0))

while not game_over:
    # Scale buildings
    building = pygame.transform.scale(building, (100, bottom_building_height))
    upside_down_building = pygame.transform.scale(upside_down_building, (100, top_building_height))

    # Render score text
    print(score)
    score_text = score_font.render(f'Score: {score}', True, score_color)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Handle key presses
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
    # Update bird position
    y += y_velocity
    y_velocity += GRAVITY

    # Update building positions
    building_x -= BUILDING_SPEED
    coin_x -= BUILDING_SPEED
    building_create = False

    if (bird_rect.colliderect(coin.get_rect())):
        superMode = True
        superScore = score
        coin_y = -1000

    if (score == superScore + 2):
        superMode = False

    # Reset building positions if they move off-screen
    if building_x < -100:  # Use a fixed width for the building
        building_x = 800
        bottom_building_height, top_building_height = new_building_sizes()
        print("generate new building")
        bird_passed_buildings = False
        building_create = True
        if (random.randint(0, 10) == 1):
            coin_y = top_building_height + 75

    if upside_down_building_x < -100:  # Use a fixed width for the building
        upside_down_building_x = 800
        print("generate new upside-down building")
        bird_passed_buildings = False
        building_create = True

    if building_create:
        score += 1

    # Update rect positions
    bird_rect.topleft = (x, y)
    building_rect = building.get_rect(topleft=(building_x, 500 - bottom_building_height))
    upside_down_building_rect = upside_down_building.get_rect(topleft=(upside_down_building_x, 0))

    # Check if bird passed the buildings and update score
    if building_rect.right < bird_rect.left and not bird_passed_buildings:
        add_score.play()
        score += 1
        bird_passed_buildings = True  # Set the flag to prevent multiple score increments

    # Check for collisions
    if bird_rect.colliderect(building_rect) or bird_rect.colliderect(upside_down_building_rect):
        if (superMode == False):
            screen.fill((0, 0, 0))
            pygame.mixer.music.stop()
            screen.blit(losing_text, (250, 200))
            pygame.display.update()
            lose_sound.play()
            time.sleep(2)
            losing_song.play()
            time.sleep(4)
            game_over = True

    # Draw everything
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(score_text, (0, 0))
    screen.blit(bird, bird_rect.topleft)
    screen.blit(upside_down_building, (building_x, 0))
    screen.blit(building, (building_x, 500 - bottom_building_height))
    screen.blit(coin, (coin_x, coin_y))
    pygame.display.update()
    clock.tick(60)

pygame.quit()