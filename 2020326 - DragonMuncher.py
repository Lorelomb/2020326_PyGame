import pygame
import sys
import random

from pygame import VIDEORESIZE
from pygame.math import Vector2


class DRAGON:
    # Dragon spawn location on the grid
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        # Dragon body part animations
        self.head_up = pygame.image.load('Assets/head up.png').convert_alpha()
        self.head_down = pygame.image.load('Assets/head down.png').convert_alpha()
        self.head_right = pygame.image.load('Assets/head right.png').convert_alpha()
        self.head_left = pygame.image.load('Assets/head left.png').convert_alpha()

        self.tail_up = pygame.image.load('Assets/tail up.png').convert_alpha()
        self.tail_down = pygame.image.load('Assets/tail down.png').convert_alpha()
        self.tail_right = pygame.image.load('Assets/tail right.png').convert_alpha()
        self.tail_left = pygame.image.load('Assets/tail left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Assets/body vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Assets/body horizontal.png').convert_alpha()

        self.curved_tr = pygame.image.load('Assets/curved top right.png').convert_alpha()
        self.curved_tl = pygame.image.load('Assets/curved top left.png').convert_alpha()
        self.curved_br = pygame.image.load('Assets/curved bottom right.png').convert_alpha()
        self.curved_bl = pygame.image.load('Assets/curved bottom left.png').convert_alpha()

    # Create a rect and then draw the dragon's body
    def draw_dragon(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        # Block version for tests
        # for block in self.body:
        #     x_pos = int(block.x * cell_size)
        #     y_pos = int(block.y * cell_size)
        #     block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        #     pygame.draw.rect(screen, (183, 111, 122), block_rect)

        for index, block in enumerate(self.body):
            # Rect for the positioning
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            # The direction the face is heading to follow up with the correct animation
            if index == 0:
                screen.blit(self.head, block_rect)
            # Check for the last item present in self.body
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                # Check if the X and Y value is the same if so vertical or horizontal body animation is played
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                # Check for the X and Y pos for the previous and next block in both directions
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.curved_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.curved_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.curved_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.curved_br, block_rect)

    # Check the first element in self.body and subtract it for the item that comes after, vector - vector = final vector
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(- 1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(- 1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_down
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_up

    # The head moves to a new block, the next bock then moves to the previous position of the head
    def move_dragon(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    # On death reset dragon's body vector to initial location on load
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class MEAT:
    def __init__(self):
        self.randomize()

    def draw_meat(self):
        meat_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(meat, meat_rect)
        # Rectangle demonstrating the food, for test purposes
        # pygame.draw.rect(screen, (126, 166, 114), meat_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = pygame.math.Vector2(self.x, self.y)


class MAIN:
    # References for the dragon and the meat to make it easier to implement other stuff in the code
    def __init__(self):
        self.dragon = DRAGON()
        self.meat = MEAT()

    # Every 0.1 second check for collision and player input
    def update(self):
        self.dragon.move_dragon()
        self.check_collision()
        self.check_fail()

    # At the start of frame draw the dragon and the meat on the main screen
    def draw_elements(self):
        self.draw_grass()
        self.meat.draw_meat()
        self.dragon.draw_dragon()
        self.draw_score()

    # This check the collision with the dragon and the meat
    def check_collision(self):
        if self.meat.pos == self.dragon.body[0]:
            self.meat.randomize()
            self.dragon.add_block()
            print("MUNCH")

        for block in self.dragon.body[1:]:
            if block == self.meat.pos:
                self.meat.randomize()

    # This will check if the dragon is outside of the screen or has hit itself
    def check_fail(self):
        if not 0 <= self.dragon.body[0].x < cell_number or not 0 <= self.dragon.body[0].y < cell_number:
            self.game_over()
        # Cycle all the dragon body blocks except for the head
        for block in self.dragon.body[1:]:
            if block == self.dragon.body[0]:
                self.game_over()

    def game_over(self):
        self.dragon.reset()

    # Draw the score using the block added to the main body
    def draw_score(self):
        score_text = str(len(self.dragon.body) - 3)
        # Controls text
        screen.blit(controls_text, (120, 5))
        # Font used on the scoreboard
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        # Position of the scoreboard
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        meat_rect = meat.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(meat_rect.left, meat_rect.top, meat_rect.width + score_rect.width + 10, meat_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(meat, meat_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    # Give the checkers look to the grass
    def draw_grass(self):
        grass_colour = (112, 162, 65)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size, cell_size,cell_size)
                        pygame.draw.rect(screen, grass_colour, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size, cell_size,cell_size)
                        pygame.draw.rect(screen, grass_colour, grass_rect)

pygame.init()
# Grid size
cell_size = 40
cell_number = 20
# Resize the grid to fit the screen when on fullscreen
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size), pygame.RESIZABLE)
clock = pygame.time.Clock()
# Load meat image
meat = pygame.image.load('Assets/turkey.png').convert_alpha()
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
# Load font for the scoreboard
game_font = pygame.font.Font('Font/Retro_Future_Curly_E_Spaced.ttf', 20)
# Load text using the font added with the set colour values
controls_text = game_font.render("Use the arrow keys to control the dragon", True, (0, 0, 0))

fullscreen = False
main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 70)

# Game loop
while True:
    # Draw all of the elements on the main display source
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == VIDEORESIZE:
            if not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            # F for fullscreen mode
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)
            # Move up
            if event.key == pygame.K_UP:
                if main_game.dragon.direction.y != 1:
                    main_game.dragon.direction = Vector2(0, -1)
            # Move to right
            if event.key == pygame.K_RIGHT:
                if main_game.dragon.direction.x != -1:
                    main_game.dragon.direction = Vector2(1, -0)
            # Move to left
            if event.key == pygame.K_LEFT:
                if main_game.dragon.direction.x != 1:
                    main_game.dragon.direction = Vector2(-1, 0)
            # Move down
            if event.key == pygame.K_DOWN:
                if main_game.dragon.direction.y != -1:
                    main_game.dragon.direction = Vector2(0, 1)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
