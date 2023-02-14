from Board import Board
import config
import pygame

class Game:
    def __init__(self, window):
        self.window = window
        self.board = Board(window)

    def update(self):
        self.board.draw()
        pygame.display.update()
    
    def mouse_to_indexes(self, pos):
        return (int(pos[0]//config.FIELD_SIZE), int(pos[1]//config.FIELD_SIZE))

    def clicked_at(self, pos):
        (col, row) = self.mouse_to_indexes(pos)
        self.board.clicked_at(row, col)
        