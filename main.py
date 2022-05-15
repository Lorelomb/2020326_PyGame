import pygame
import sys
import random

from pygame import VIDEORESIZE
from pygame.math import Vector2


class DRAGON:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    # Create a rect and then draw the dragon's body
    def draw_dragon(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

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

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class MEAT:
    def __init__(self):
        self.randomize()

    def draw_meat(self):
        meat_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(meat, meat_rect)
        pygame.draw.rect(screen, (126, 166, 114), meat_rect)

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

    def draw_score(self):
        score_text = str(len(self.dragon.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 1080)
        score_y = int(cell_size * cell_number - 1150)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        meat_rect = meat.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(meat_rect.left, meat_rect.top, meat_rect.width + score_rect.width + 6, meat_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(meat, meat_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 3)


pygame.init()
cell_size = 40
cell_number = 30
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size), pygame.RESIZABLE)
clock = pygame.time.Clock()
meat = pygame.image.load('Assets/turkey.png').convert_alpha()
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
game_font = pygame.font.Font('Font/Retro_Future_Curly_E_Spaced.ttf', 25)

fullscreen = False
main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 60)

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
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)
            if event.key == pygame.K_UP:
                if main_game.dragon.direction.y != 1:
                    main_game.dragon.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main_game.dragon.direction.x != -1:
                    main_game.dragon.direction = Vector2(1, -0)
            if event.key == pygame.K_LEFT:
                if main_game.dragon.direction.x != 1:
                    main_game.dragon.direction = Vector2(-1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.dragon.direction.y != -1:
                    main_game.dragon.direction = Vector2(0, 1)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
