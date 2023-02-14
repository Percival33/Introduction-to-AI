from Pawn import Pawn
import config
import pygame


class King(Pawn):
    def __init__(self, pawn):
        super().__init__(pawn.is_white(), pawn.window, pawn.row, pawn.col, pawn.board)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__dict__.update(self.__dict__)
        return result

    def is_king(self):
        return True

    def __str__(self):
        if self.is_white():
            return "W"
        return "B"

    def draw(self):
        if self.is_white():
            cur_col = config.WHITE
        else:
            cur_col = config.BLUE
        x = self.col * config.FIELD_SIZE
        y = self.row * config.FIELD_SIZE
        pygame.draw.circle(self.window, cur_col, (x + config.FIELD_SIZE / 2, y + config.FIELD_SIZE / 2),
                           config.PIECE_SIZE)
        pygame.draw.circle(self.window, config.GREEN, (x + config.FIELD_SIZE / 2, y + config.FIELD_SIZE / 2),
                           config.PIECE_SIZE / 2)

        if self.is_marked():
            pygame.draw.circle(self.window, config.RED, (x + config.FIELD_SIZE / 2, y + config.FIELD_SIZE / 2),
                               config.PIECE_SIZE + config.MARK_THICK, config.MARK_THICK)
