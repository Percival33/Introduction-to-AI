class Move:
    def __init__(self, piece, dest_row, dest_col, captures=None):
        self.piece = piece
        self.dest_row = dest_row
        self.dest_col = dest_col
        self.captures = captures

    def __str__(self):
        return f'piece: {self.piece} dest(r,c): ({self.dest_row}, {self.dest_col}) captures: {self.captures}'
