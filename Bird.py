import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
GRAVITY = 0.5
JUMP_VELOCITY = -4
PIPE_SPEED = 3
GAP_SIZE = 150
WHITE = (255, 255, 255)


class Bird:
    def __init__(self):
        self.image = pygame.image.load('./images/Flappy-Bird-PNG-File.png')
        self.image = pygame.transform.scale(self.image, (100, 50))
        self.x, self.y = 100, SCREEN_HEIGHT // 2
        self.y_velocity = 0
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def reset(self):
        self.x, self.y = 100, SCREEN_HEIGHT // 2
        self.y_velocity = 0

    def jump(self):
        self.y_velocity = JUMP_VELOCITY

    def update(self):
        self.y += self.y_velocity
        self.y_velocity += GRAVITY
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
