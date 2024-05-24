import pygame, sys
from game import Game
from colors import Colors

pygame.init()
title_font = pygame.font.Font(None,40)
score_surface = title_font.render('Score',True,(255,255,255))
next_surface = title_font.render('Next',True,Colors.white)
game_over_surface = title_font.render('GAME OVER', True, Colors.white)
score_rect = pygame.Rect(320,55,170,60)
next_rect = pygame.Rect(320,215,170,180)
dark_blue = (44,44,127)

screen = pygame.display.set_mode((500,620))
pygame.display.set_caption('Python Tetris')

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.game_over == True:
                game.game_over = False  # Fix: Use assignment operator (=) instead of equality check (==)
                game.reset()  # Fix: Add parentheses to call the reset method
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
        if event.type == GAME_UPDATE:
            game.move_down()

# ... (rest of your code)



screen.fill(Colors.dark_blue)
screen.blit(score_surface,(365,20,50,50))
screen.blit(next_surface,(375,180,50,50))
if game.gamer_over == True:
    screen.blit(game_over_surface,(320,450,50,50))

pygame.draw.rect(screen, Colors.light_blue, score_rect, 0,10)
pygame.draw.rect(screen,Colors.light_blue, next_rect, 0,10)
game.draw(screen)

pygame.display.update()
clock.tick(60)
from grid import Grid
from blocks import *
import random
import pygame

import pygame
import random

class Game:
    def __init__(self):
        # Initialize the game with a grid, a set of blocks, and game-related variables
        self.grid = Grid()  # Assuming Grid class is defined elsewhere
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]  # Initialize all block types
        self.current_block = self.get_random_block()  # Set the current block to a random block
        self.next_block = self.get_random_block()  # Set the next block to a random block
        self.game_over = False  # Flag to track game over state
        self.score = 0  # Variable to track the player's score
        self.rotate_sound = pygame.mixer.Sound("rotate.ogg")  # Sound for block rotation
        self.clear_sound = pygame.mixer.Sound("clear.ogg")  # Sound for clearing rows

        # Load and play background music
        pygame.mixer.music.load("Tetris Remix.mp3")
        pygame.mixer.music.play(-1)

    # Update the player's score based on cleared lines and downward movements
    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points

    # Get a random block from the available block types, replenishing the list if empty
    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    # Move the current block left, checking for collisions
    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    # Move the current block right, checking for collisions
    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    # Move the current block down, checking for collisions; lock the block if it cannot move further down
    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()

    # Lock the current block on the grid, check for cleared rows, update the score, and handle game over conditions
    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if self.block_fits() == False:
            self.game_over = True

    # Reset the game state
    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    # Check if the current block fits on the grid
    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    # Rotate the current block, checking for collisions and playing a sound if successful
    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.play()

    # Check if the current block is entirely inside the grid
    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    # Draw the grid, the current block, and the next block on the screen
    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        # Draw the next block at different positions based on the block type
        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)
            from colors import Colors
import pygame
from position import Position

import pygame

class Position:
    def __init__(self, row, column):
        # Initialize a position with given row and column values
        self.row = row
        self.column = column

class Block:
    def __init__(self, id):
        # Initialize a block with a unique identifier
        self.id = id
        self.cells = {}
        self.cell_size = 30  # Size of each cell in pixels
        self.row_offset = 0  # Offset for the row position
        self.column_offset = 0  # Offset for the column position
        self.rotation_state = 0  # Current rotation state
        self.colors = Colors.get_cell_colors()  # Assuming Colors.get_cell_colors() returns a dictionary of colors

    def move(self, rows, columns):
        # Move the block by adjusting the row and column offsets
        self.row_offset += rows
        self.column_offset += columns

    def get_cell_positions(self):
        # Get the positions of the cells in the current rotation state, considering offsets
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles

    def rotate(self):
        # Rotate the block clockwise
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotation(self):
        # Undo the last rotation
        self.rotation_state -= 1
        if self.rotation_state == -1:
            self.rotation_state = len(self.cells) - 1

    def draw(self, screen, offset_x, offset_y):
        # Draw the block on the screen at the specified position
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size,
                                    offset_y + tile.row * self.cell_size, self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)
            from block import Block
from position import Position

class LBlock(Block):
    def __init__(self):
        # Initialize an L-shaped block
        super().__init__(id=1)
        self.cells = {
            0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
            3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

class JBlock(Block):
    def __init__(self):
        # Initialize a J-shaped block
        super().__init__(id=2)
        self.cells = {
            0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
            3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
        }
        self.move(0, 3)

class IBlock(Block):
    def __init__(self):
        # Initialize an I-shaped block
        super().__init__(id=3)
        self.cells = {
            0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
            1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
            2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
            3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
        }
        self.move(-1, 3)

class OBlock(Block):
    def __init__(self):
        # Initialize an O-shaped block
        super().__init__(id=4)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)]
        }
        self.move(0, 4)

class SBlock(Block):
    def __init__(self):
        # Initialize an S-shaped block
        super().__init__(id=5)
        self.cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
            2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
            3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

class TBlock(Block):
    def __init__(self):
        # Initialize a T-shaped block
        super().__init__(id=6)
        self.cells = {
            0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

class ZBlock(Block):
    def __init__(self):
        # Initialize a Z-shaped block
        super().__init__(id=7)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
            1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
        }
        self.move(0, 3)
        import pygame
from colors import Colors
class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)]for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end=" ")
            print()


    def is_inside(self,row, column):
        if row >= 0 and row < self.num_rows and column >=0 and column < self.num_cols:
            return True
        return False

    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
            return True

    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row+num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clear_full_row(self,row):
        completed = 0
        for row in range(self.num_rows-1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed
    


    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    def draw(self, screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column*self.cell_size +11, row*self.cell_size +11, self.cell_size-1, self.cell_size-1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)

