from typing import Tuple
from src.constant import ColorConstant, ShapeConstant
from src.model.piece import Piece


class Board:
    """
    Class representation class for Board used in game

    [ATTRIBUTES]
        row: int -> boards row shape
        col: int -> boards column shape
        board: 2D List -> board representation
    """

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.board = [
            [Piece(ShapeConstant.BLANK, ColorConstant.BLACK) for i in range(self.col)]
            for j in range(self.row)
        ]

    def __str__(self):
        ret = ""

        temp_num = 0
        for col in range(self.col * 6 + 1):
            if col % 6 == 3:
                ret += str(temp_num)
                temp_num += 1
            else:
                ret += ' '
        ret += '\n'

        el_row = 0
        el_col = 0
        for row in range(self.row * 2 + 1):
            if row % 2 == 0:
                for col in range(self.col * 6 + 1):
                    if col % 6 == 0:
                        ret += '.'
                    elif col % 6 in [1, 5]:
                        ret += ' '
                    elif col % 6 in [2, 4]:
                        ret += '-'
                    elif col % 6 == 3:
                        ret += '='
            else:
                for col in range(self.col * 6 + 1):
                    if col % 6 == 0:
                        ret += "|"
                    elif col % 6 in [1, 2, 4, 5]:
                        ret += ' '
                    elif col % 6 == 3:
                        ret += self.board[el_row][el_col].__str__()
                        el_col += 1
                el_row += 1
                el_col = 0
            ret += "\n"
        return ret

    def __getitem__(self, pos: Tuple[int, int]):
        row, col = pos
        return self.board[row][col]

    def set_piece(self, row: int, col: int, piece: Piece):
        self.board[row][col] = piece
