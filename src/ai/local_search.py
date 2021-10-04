from time import time
from typing import Tuple

from src.constant import GameConstant, ShapeConstant
from src.model import State, Board
from src.utility import is_out


class LocalSearch:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        best_movement = (
            self.objective_func(state, n_player, thinking_time), state.players[n_player].shape)

        return best_movement

    @staticmethod
    def check_heuristic(board: Board, row: int, col: int):
        # yes i reused check_streak, no im not ashamed
        """
        [DESC] fungsi utk dapat value heuristik piece di board[row][col]
        [RETURN]
        0 if board[row][col] kosong
        int if ada isinya
        """
        piece = board[row, col]

        streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        mark = 0

        for prior in GameConstant.WIN_PRIOR:
            for row_ax, col_ax in streak_way:
                row_ = row + row_ax
                col_ = col + col_ax
                for _ in range(10):  # since board is 6x7, 10 should be fine to check all cardinal directions
                    if is_out(board, row_, col_):
                        mark += 0
                        break
                    shape_condition = (  # true if shape different
                            prior == GameConstant.SHAPE
                            and piece.shape != board[row_, col_].shape
                    )
                    color_condition = (  # true if color different
                            prior == GameConstant.COLOR
                            and piece.color != board[row_, col_].color
                    )
                    if board[row_, col_].shape == ShapeConstant.BLANK:  # if meet blank piece
                        mark += 0
                    else:
                        if (not shape_condition) and (not color_condition):  # same color shape
                            mark += 3
                        elif (not shape_condition) and color_condition:  # same shape
                            mark += 1
                        elif shape_condition and (not color_condition):  # same color
                            mark -= 1
                        elif shape_condition and color_condition:  # none same
                            mark -= 3
                    row_ += row_ax
                    col_ += col_ax

        return mark

    @staticmethod
    def objective_func(state: State, n_player: int, thinking_time: float):
        current_board = state.board
        mark = -999
        # default if all of the columns are empty (first move) prefer yg ditengah
        column_choice = current_board.col // 2
        for i in range(current_board.col):
            for j in range(current_board.row):  # cek dari atas ke bawah bcs kyk gini strukturnya
                # check for first piece thats not a blank in each column
                if current_board[j, i].shape != ShapeConstant.BLANK:
                    if j == current_board.row - 1:  # top most row of current column is filled
                        break
                current_mark = LocalSearch.check_heuristic(current_board, j + 1, i)
                if current_mark >= mark:  # change column choice
                    column_choice = i
                mark = max(current_mark, mark)
        return column_choice
