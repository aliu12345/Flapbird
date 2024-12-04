import pygame
import random
import Assets

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
GRAVITY = 0.5
JUMP_VELOCITY = -4
PIPE_SPEED = 3
GAP_SIZE = 150
WHITE = (255, 255, 255)

class PipeManager:
    def __init__(self):
        self.vertical_speed = 1
        self.pipe_image = pygame.image.load('./images/pipe.png')
        self.upside_down_pipe_image = pygame.image.load("./images/upside_down_pipe.png")
        self.pipe_x = SCREEN_WIDTH
        self.bottom_pipe_height, self.top_pipe_height = self.generate_pipe_heights()
        self.bird_passed = False
        self.pipes = []  # Stores pipe pairs as tuples (top_pipe_rect, bottom_pipe_rect, passed_flag)
        self.vertical_offset = 0
        self.pipe_speed = PIPE_SPEED
        self.gap_size = GAP_SIZE
        self.vertical_direction = 1  # 1 for down, -1 for u
        self.max_vertical_movement = 50
        self.assets = Assets.Assets()
        self.pipes = []  # Store tuples of (top_pipe_rect, bottom_pipe_rect, passed_flag, movement_type)
        self.vertical_offset = 0
        self.pipe_speed = PIPE_SPEED
        self.gap_size = GAP_SIZE
        self.vertical_direction = 1  # 1 for down, -1 for up
        self.vertical_speed = 1
        self.horizontal_speed = 2  # Speed of horizontal extension/retraction
        self.max_width_extension = 30  # Maximum width change for extending pipes


    def reset(self):
        self.pipes.clear()
        self.vertical_direction = 1
        self.vertical_offset = 0
        self.add_pipe_pair()

    def add_pipe_pair(self):
        # Restrict pipe height to be within a reasonable range
        min_pipe_height = 50
        max_pipe_height = SCREEN_HEIGHT - self.gap_size - min_pipe_height

        # Randomize pipe heights
        pipe_top_height = random.randint(min_pipe_height, max_pipe_height)
        pipe_bottom_height = SCREEN_HEIGHT - pipe_top_height - self.gap_size

        # Create pipes at the screen's right edge
        pipe_top_rect = pygame.Rect(SCREEN_WIDTH, 0, 50, pipe_top_height)
        pipe_bottom_rect = pygame.Rect(SCREEN_WIDTH, SCREEN_HEIGHT - pipe_bottom_height, 50, pipe_bottom_height)

        self.pipes.append((pipe_top_rect, pipe_bottom_rect, False))  # `False` means not yet passed

    def generate_pipe_heights(self):
        bottom_height = random.randint(100, 300)
        top_height = SCREEN_HEIGHT - GAP_SIZE - bottom_height
        return bottom_height, top_height

    def get_pipes(self):
        # Flatten and return all pipe rectangles for collision checks
        return [pipe for pair in self.pipes for pipe in pair]


    def update(self, bird_rect):
        # Move pipes horizontally
        for i in range(len(self.pipes)):
            self.pipes[i] = (
                self.pipes[i][0].move(-self.pipe_speed, 0),
                self.pipes[i][1].move(-self.pipe_speed, 0),
                self.pipes[i][2],  # Preserve the passed flag
            )

        # Remove pipes that have moved off screen
        self.pipes = [pair for pair in self.pipes if pair[0].right > 0]

        # Add new pipe pair if needed
        if not self.pipes or self.pipes[-1][0].x < SCREEN_WIDTH - 200:
            self.add_pipe_pair()

        # Move pipes vertically
        self.vertical_offset += self.vertical_speed * self.vertical_direction
        if abs(self.vertical_offset) > self.max_vertical_movement:
            self.vertical_direction *= -1  # Reverse direction when hitting limit


        for i in range(len(self.pipes)):
            pipe_top, pipe_bottom, passed = self.pipes[i]
            if i % 2 == 0:

                self.pipes[i] = (
                    pipe_top.move(0, self.vertical_speed * -self.vertical_direction),
                    pipe_bottom.move(0, self.vertical_speed * self.vertical_direction),
                    passed,
                )
            else:
                self.pipes[i] = (
                    pipe_top.move(0, self.vertical_speed * self.vertical_direction),
                    pipe_bottom.move(0, self.vertical_speed * self.vertical_direction),
                    passed,
                )


        # Check if the bird has passed any pipes
        score_increment = 0
        for i in range(len(self.pipes)):
            pipe_top, pipe_bottom, passed = self.pipes[i]
            if not passed and bird_rect.left > pipe_top.right:
                self.pipes[i] = (pipe_top, pipe_bottom, True)  # Mark as passed
                score_increment += 1

        return score_increment

    def get_pipes(self):
        bottom_pipe = self.pipe_image.get_rect(topleft=(self.pipe_x, SCREEN_HEIGHT - self.bottom_pipe_height))
        top_pipe = self.upside_down_pipe_image.get_rect(topleft=(self.pipe_x, 0))
        return [bottom_pipe, top_pipe]

    def pass_pipe(self, bird_rect):
        if not self.bird_passed and bird_rect.left > self.pipe_x + 100:
            self.bird_passed = True
            return True
        return False

    def check_collisions(self, bird_rect):
        for pipe_top, pipe_bottom, _ in self.pipes:
            if bird_rect.colliderect(pipe_top) or bird_rect.colliderect(pipe_bottom):
                return True  # Collision detected
        return False

    def draw(self, surface):
        for pipe_top, pipe_bottom, _ in self.pipes:
            # Scale images to fit pipe dimensions
            pipe_top_image = pygame.transform.scale(
                self.assets.pipe_top_image, (pipe_top.width, pipe_top.height)
            )
            pipe_bottom_image = pygame.transform.scale(
                self.assets.pipe_bottom_image, (pipe_bottom.width, pipe_bottom.height)
            )
            # Draw pipe images
            surface.blit(pipe_top_image, (pipe_top.x, pipe_top.y))
            surface.blit(pipe_bottom_image, (pipe_bottom.x, pipe_bottom.y))
