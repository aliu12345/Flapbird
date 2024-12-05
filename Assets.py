import pygame
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
GRAVITY = 0.5
JUMP_VELOCITY = -4
PIPE_SPEED = 3
GAP_SIZE = 150
WHITE = (255, 255, 255)


class Assets:
    def __init__(self):
        self.background = pygame.image.load('./images/background.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_over_font = pygame.font.SysFont('Arial', 20)
        self.score_font = pygame.font.SysFont('Arial', 50)
        self.losing_font = pygame.font.SysFont('Arial', 50)
        self.pipe_top_image = pygame.image.load('./images/pipe.png')
        self.pipe_bottom_image = pygame.image.load('./images/upside_down_pipe.png')
        self.final_score_font = pygame.font.SysFont('Arial', 30)

        # Define separate positions for buttons
        self.quit_button = pygame.Rect((SCREEN_WIDTH - 100), SCREEN_HEIGHT - 50, 100, 50)
        self.start_over_button = pygame.Rect((SCREEN_WIDTH - 445), 350, 100, 50)

        # Render button text
        self.quit_button_text = self.final_score_font.render("Quit", True, WHITE)
        self.start_over_button_text = self.start_over_font.render("Start Over", True, WHITE)

        # Sounds
        self.jump_sound = pygame.mixer.Sound('./sounds/Jump.wav')
        self.coin_sound = pygame.mixer.Sound("./sounds/Coin.wav")
        self.lose_sound = pygame.mixer.Sound("./sounds/Womp Womp Womp sound effect.wav")
        self.background_music = pygame.mixer.music.load('./sounds/Music.mp3')

    def play_background_music(self):
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_lose_sounds(self):
        self.lose_sound.play()
        time.sleep(2)  # Wait for sound effect

