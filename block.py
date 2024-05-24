from colors import Colors
import pygame
from position import Position



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
