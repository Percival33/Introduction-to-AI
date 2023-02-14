from copy import deepcopy
from Field import Field
from Move import Move
from King import King
from Pawn import Pawn
import config
import pygame


class Board:
    def __init__(self, window):  # row, col
        self.board = []  # np.full((BOARD_WIDTH, BOARD_WIDTH), None)
        self.window = window
        self.marked_piece = None
        self.something_is_marked = False
        self.white_turn = True
        self.white_fig_left = 12
        self.blue_fig_left = 12

        self.__set_pieces()

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__dict__.update(self.__dict__)
        result.board = deepcopy(self.board)
        return result

    def __str__(self):
        to_ret = ""
        for row in range(8):
            for col in range(8):
                to_ret += str(self.board[row][col])
            to_ret += "\n"
        return to_ret

    def __set_pieces(self):
        for row in range(8):
            self.board.append([])
            for col in range(8):
                self.board[row].append(Field())

        for row in range(3):
            for col in range((row + 1) % 2, config.BOARD_WIDTH, 2):
                self.board[row][col] = Pawn(False, self.window, row, col, self)

        for row in range(5, 8):
            for col in range((row + 1) % 2, config.BOARD_WIDTH, 2):
                self.board[row][col] = Pawn(True, self.window, row, col, self)

    def get_piece_moves(self, piece):
        pos_moves = []
        row = piece.row
        col = piece.col
        if piece.is_blue():
            enemy_is_white = True
        else:
            enemy_is_white = False

        if piece.is_white() or (piece.is_blue() and piece.is_king()):
            dir_y = -1
            if row > 0:
                new_row = row + dir_y
                if col > 0:
                    new_col = col - 1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece, new_row, new_col))
                        # ruch zwiazany z biciem
                    elif self.board[new_row][new_col].is_white() == enemy_is_white \
                            and new_row + dir_y >= 0 and new_col - 1 >= 0 and \
                            self.board[new_row + dir_y][new_col - 1].is_empty():
                        pos_moves.append(Move(piece, new_row + dir_y, new_col - 1, self.board[new_row][new_col]))

                if col < config.BOARD_WIDTH - 1:
                    new_col = col + 1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece, new_row, new_col))
                        # ruch zwiazany z biciem
                    elif self.board[new_row][new_col].is_white() == enemy_is_white \
                            and new_row + dir_y >= 0 and new_col + 1 < config.BOARD_WIDTH and \
                            self.board[new_row + dir_y][new_col + 1].is_empty():
                        pos_moves.append(Move(piece, new_row + dir_y, new_col + 1, self.board[new_row][new_col]))

        if piece.is_blue() or (piece.is_white() and self.board[row][col].is_king()):
            dir_y = 1
            if row < config.BOARD_WIDTH - 1:
                new_row = row + dir_y
                if col > 0:
                    new_col = col - 1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece, new_row, new_col))
                    elif self.board[new_row][
                        new_col].is_white() == enemy_is_white and new_row + dir_y < config.BOARD_WIDTH and \
                            new_col - 1 >= 0 and self.board[new_row + dir_y][new_col - 1].is_empty():
                        pos_moves.append(Move(piece, new_row + dir_y, new_col - 1, self.board[new_row][new_col]))

                if col < config.BOARD_WIDTH - 1:
                    new_col = col + 1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece, new_row, new_col))
                        # ruch zwiazany z bicie!
                    elif self.board[new_row][new_col].is_white() == enemy_is_white and \
                            new_row + dir_y < config.BOARD_WIDTH and new_col + 1 < config.BOARD_WIDTH and \
                            self.board[new_row + dir_y][new_col + 1].is_empty():
                        pos_moves.append(Move(piece, new_row + dir_y, new_col + 1, self.board[new_row][new_col]))
        return pos_moves

    def evaluate(self, is_blue_turn):
        # func 1
        def is_valid(curr_row, curr_col):
            return 0 <= curr_row < config.BOARD_WIDTH and 0 <= curr_col < config.BOARD_WIDTH

        def get_points(curr_row, curr_col, is_blue):
            points = 0
            if is_valid(curr_row + 1, curr_col - 1) and not self.board[curr_row + 1][curr_col - 1].is_empty() and \
                    is_blue == self.board[curr_row + 1][curr_col - 1].is_blue():
                points += 1
            if is_valid(curr_row + 1, curr_col + 1) and not self.board[curr_row + 1][curr_col + 1].is_empty() and \
                    is_blue == self.board[curr_row + 1][curr_col + 1].is_blue():
                points += 1

            return points

        # func 3
        # def get_points(curr_row, is_blue):
        #     blue_points = (curr_row + 1) * 5
        #     white_points = (config.BOARD_WIDTH - curr_row) * 5
        #     return blue_points if is_blue else white_points

        # func 2
        # def get_points(curr_row, is_blue):
        #     blue_points = 5 if curr_row < config.BOARD_WIDTH // 2 else 7
        #     white_points = 5 if curr_row >= config.BOARD_WIDTH // 2 else 7
        #     return blue_points if is_blue else white_points

        h = 0
        h_blue = 0
        h_white = 0
        for row in range(config.BOARD_WIDTH):
            for col in range((row + 1) % 2, config.BOARD_WIDTH, 2):
                if self.board[row][col].is_empty():
                    continue
                # print(f'(r,c)=({row},{col}) blue={self.board[row][col].is_blue()} white={self.board[row][col].is_white()}')
                point = 10 if self.board[row][col].is_king() else 1

                tmp = get_points(row, col, self.board[row][col].is_blue())

                h_blue += point + tmp if self.board[row][col].is_blue() else 0
                h_white += point + tmp if self.board[row][col].is_white() else 0

        diff = h_blue - h_white
        return diff if is_blue_turn else -1 * diff

    def get_possible_moves(self, is_blue_turn):
        pos_moves = []
        for row in range(config.BOARD_WIDTH):
            for col in range((row + 1) % 2, config.BOARD_WIDTH, 2):
                if not self.board[row][col].is_empty():
                    if (is_blue_turn and self.board[row][col].is_blue()) or \
                            (not is_blue_turn and self.board[row][col].is_white()):
                        pos_moves.extend(self.get_piece_moves(self.board[row][col]))
        return pos_moves

    def draw(self):
        self.window.fill(config.WHITE)
        for row in range(config.BOARD_WIDTH):
            for col in range((row + 1) % 2, config.BOARD_WIDTH, 2):
                y = row * config.FIELD_SIZE
                x = col * config.FIELD_SIZE
                pygame.draw.rect(self.window, config.BLACK, (x, y, config.FIELD_SIZE, config.FIELD_SIZE))
                self.board[row][col].draw()

    def move(self, field):
        d_row = field.row
        d_col = field.col
        row_from = field.row_from
        col_from = field.col_from
        self.board[row_from][col_from].toggle_mark()
        self.something_is_marked = False
        self.board[d_row][d_col] = self.board[row_from][col_from]
        self.board[d_row][d_col].row = d_row
        self.board[d_row][d_col].col = d_col
        self.board[row_from][col_from] = Field()

        if field.pos_move.captures:
            fig_to_del = field.pos_move.captures

            self.board[fig_to_del.row][fig_to_del.col] = Field()
            if self.white_turn:
                self.blue_fig_left -= 1
            else:
                self.white_fig_left -= 1

        if self.white_turn and d_row == 0:  # damka
            self.board[d_row][d_col] = King(self.board[d_row][d_col])

        if not self.white_turn and d_row == config.BOARD_WIDTH - 1:  # damka
            self.board[d_row][d_col] = King(self.board[d_row][d_col])

        self.white_turn = not self.white_turn

    def end(self):
        return self.white_fig_left == 0 or self.blue_fig_left == 0 or len(
            self.get_possible_moves(not self.white_turn)) == 0

    def clicked_at(self, row, col):
        field = self.board[row][col]
        if field.is_move_mark():
            self.move(field)
        if (field.is_white() and self.white_turn and not self.something_is_marked) or (
                field.is_blue() and not self.white_turn and not self.something_is_marked):
            field.toggle_mark()
            self.something_is_marked = True
        elif self.something_is_marked and field.is_marked():
            field.toggle_mark()
            self.something_is_marked = False

    # tu spore powtorzenie kodu z move
    def make_ai_move(self, move):
        d_row = move.dest_row
        d_col = move.dest_col
        row_from = move.piece.row
        col_from = move.piece.col

        self.board[d_row][d_col] = self.board[row_from][col_from]
        self.board[d_row][d_col].row = d_row
        self.board[d_row][d_col].col = d_col
        self.board[row_from][col_from] = Field()

        if move.captures:
            fig_to_del = move.captures

            self.board[fig_to_del.row][fig_to_del.col] = Field()
            if self.white_turn:
                self.blue_fig_left -= 1
            else:
                self.white_fig_left -= 1

        if self.white_turn and d_row == 0:  # damka
            self.board[d_row][d_col] = King(self.board[d_row][d_col])

        if not self.white_turn and d_row == config.BOARD_WIDTH - 1:  # damka
            self.board[d_row][d_col] = King(self.board[d_row][d_col])

        self.white_turn = not self.white_turn
