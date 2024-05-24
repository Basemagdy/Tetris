from grid import Grid
from blocks import *
import random
import pygame

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
        pygame.mixer.music.load("music.ogg")
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
