import pygame
import sys
import random
from pygame.math import Vector2


class DRAGON:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
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



class MEAT:
    def __init__(self):
        self.randomize()

    def draw_meat(self):
        meat_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (126, 166, 114), meat_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = pygame.math.Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.dragon = DRAGON()
        self.meat = MEAT()

    def update(self):
        self.dragon.move_dragon()
        self.check_collision()

    def draw_elements(self):
        self.meat.draw_meat()
        self.dragon.draw_dragon()

    def check_collision(self):
        if self.meat.pos == self.dragon.body[0]:
            self.meat.randomize()
            self.dragon.add_block()
            print("MUNCH")


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)


while True:
    # Draw all of the elements on the main display source
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                main_game.dragon.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                main_game.dragon.direction = Vector2(1, -0)
            if event.key == pygame.K_LEFT:
                main_game.dragon.direction = Vector2(-1, 0)
            if event.key == pygame.K_DOWN:
                main_game.dragon.direction = Vector2(0, 1)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
