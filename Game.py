

import pygame
import Bird
import PipeManager
import Assets
from pygame.locals import *

# Initialize pygame
pygame.mixer.init()
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
GRAVITY = 0.5
JUMP_VELOCITY = -4
PIPE_SPEED = 3
GAP_SIZE = 150
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BUTTON_COLOR = (0, 0, 170)
BUTTON_OVER_COLOR = (250, 50, 50)
START_OVER_BUTTON_COLOR = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

class FlappyBirdGame:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.paused = False
        self.game_over = False
        self.bird = Bird.Bird()
        self.pipe_manager = PipeManager.PipeManager()
        self.assets = Assets.Assets()
        self.assets.play_background_music()
        self.pause_button = pygame.Rect(10, 60, 100, 50)  # Pause button


    def reset_game(self):
        self.bird.reset()  # Reset bird position and state
        self.pipe_manager.reset()  # Reset pipes
        self.score = 0  # Reset score
        self.paused = False  # Resume the game
        self.game_over = False  # Set game over to False
        self.assets.play_background_music()  # Restart background music

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    # Handle buttons during game-over screen
                    if self.assets.quit_button.collidepoint(event.pos):
                        print("Quit button clicked!")
                        self.running = False
                    if self.assets.start_over_button.collidepoint(event.pos):
                        print("Start Over button clicked!")
                        self.reset_game()
                elif not self.paused:  # Normal game inputs
                    if self.pause_button.collidepoint(event.pos):
                        self.paused = not self.paused
                else:
                    if self.pause_button.collidepoint(event.pos):
                        self.paused = not self.paused
                if not self.game_over and not self.paused:
                    self.bird.jump()
                    self.assets.jump_sound.play()
            if event.type == pygame.KEYDOWN and not self.game_over and not self.paused:
                if event.key in [K_SPACE, K_w, K_UP]:
                    self.bird.jump()
                    self.assets.jump_sound.play()

    def update(self):
        if not self.paused and not self.game_over:
            self.bird.update()
            score_increment = self.pipe_manager.update(self.bird.rect)  # Update pipes and check scoring
            self.score += score_increment

            if self.bird.y > SCREEN_HEIGHT:
                self.end_game()
            if self.bird.y < 0:
                self.end_game()

            # Check for collisions
            if self.pipe_manager.check_collisions(self.bird.rect):
                self.end_game()  # End the game if the bird collides


    def check_collisions(self):
        if self.bird.y > SCREEN_HEIGHT - self.bird.rect.height or self.bird.y < 0:
            self.end_game()

        for pipe_rect in self.pipe_manager.get_pipes():
            if self.bird.rect.colliderect(pipe_rect):
                self.end_game()

        if self.pipe_manager.pass_pipe(self.bird.rect):
            self.score += 1
            self.assets.coin_sound.play()

    def end_game(self):
        self.game_over = True
        print("game over")
        self.assets.stop_music()

    def check_collisions(self, bird_rect):
        for pipe_top, pipe_bottom, _ in self.pipes:
            if bird_rect.colliderect(pipe_top) or bird_rect.colliderect(pipe_bottom):
                return True  # Collision detected
        return False

    def redraw(self):
        screen.blit(self.assets.background, (0, 0))
        self.pipe_manager.draw(screen)
        self.bird.draw(screen)
        self.draw_score()

    def draw(self):
        self.redraw()
        self.draw_pause_button()  # Draw pause button
        pygame.display.update()


    def draw_score(self):
        score_text = self.assets.score_font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    def draw_pause_button(self):
        # Draw pause button with appropriate text
        button_text = "Pause"
        if self.paused:
            button_text = "Resume"
        pygame.draw.rect(screen, BUTTON_COLOR, self.pause_button)
        text_surface = self.assets.final_score_font.render(button_text, True, WHITE)
        screen.blit(text_surface, (self.pause_button.x + (self.pause_button.width - text_surface.get_width()) // 2,
                                   self.pause_button.y + (self.pause_button.height - text_surface.get_height()) // 2))
    def draw_game_over_buttons(self):
        pygame.draw.rect(screen, START_OVER_BUTTON_COLOR, self.assets.start_over_button)
        screen.blit(self.assets.start_over_button_text, (
            self.assets.start_over_button.x + (
                    self.assets.start_over_button.width - self.assets.start_over_button_text.get_width()) // 2,
            self.assets.start_over_button.y + (
                    self.assets.start_over_button.height - self.assets.start_over_button_text.get_height()) // 2
        ))

        # Draw "Quit" button
        pygame.draw.rect(screen, BUTTON_COLOR, self.assets.quit_button)
        screen.blit(self.assets.quit_button_text,
                    (((
                                  self.assets.quit_button.width - self.assets.quit_button_text.get_width()) / 2 + self.assets.quit_button.left),
                     (SCREEN_HEIGHT - self.assets.quit_button_text.get_height())))
    def dim_screen(self):
        dim_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)  # Use SRCALPHA for transparency
        dim_surface.fill((0, 0, 0, 128))  # RGBA: Black color with 128 alpha for transparency
        screen.blit(dim_surface, (0, 0))

    def draw_final_score_text(self):
        final_score_text = self.assets.final_score_font.render(f"Your score: {self.score}", True, WHITE)
        screen.blit(final_score_text, (SCREEN_WIDTH / 2 - final_score_text.get_width() / 2, 250))
    def draw_game_over_text(self):
        game_over_text = self.assets.losing_font.render("Game Over", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() / 2, 150))
    def draw_game_over_screen(self):
        # Redraw the previous frame and dim it
        self.redraw()
        self.dim_screen()
        self.draw_final_score_text()
        self.draw_game_over_text()
        self.draw_game_over_buttons()


    def run(self):
        while self.running:
            self.handle_events()
            if not self.game_over:
                self.update()
                self.draw()
            else:
                self.draw_game_over_screen()
                pygame.display.update()  # Ensure game-over screen updates
            self.clock.tick(FPS)
        pygame.quit()
