from Field import Field
from copy import deepcopy
import pygame
import config

class PosMoveField(Field):
    def __init__(self, is_white, window, row, col, board, row_from, col_from, pos_move):
        self.__is_white=is_white
        self.__is_marked =False 
        self.window = window
        self.row = row
        self.col = col
        self.board = board
        self.row_from = row_from
        self.col_from = col_from
        self.pos_move=pos_move
        
            
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__dict__.update(self.__dict__)
        return result                
        
    def draw(self):
        x = self.col*config.FIELD_SIZE
        y = self.row*config.FIELD_SIZE
        pygame.draw.circle(self.window, config.RED, (x+config.FIELD_SIZE/2, y+config.FIELD_SIZE/2), config.POS_MOVE_MARK_SIZE)
    
    def is_empty(self):
        return True
        
    def is_move_mark(self):
        return True
