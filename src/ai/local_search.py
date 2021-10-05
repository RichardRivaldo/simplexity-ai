from math import exp
from time import time
from typing import Tuple

from src.constant import GameConstant, ShapeConstant
from src.model import Board, State
from src.utility import is_out, place


class LocalSearch:
    def __init__(self):
        pass

    def find(
        self, state: State, n_player: int, thinking_time: float
    ) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        if self.is_empty(state.board):
            return (state.board.col // 2, state.players[n_player].shape)

        best_movement = (
            self.hill_climbing(state, n_player, thinking_time),
            state.players[n_player].shape,
        )

        return best_movement

    def is_valid_move(state: State, piece, column):
        return place()

    def find_possible_moves(state: State):
        print(state.board)

    @staticmethod
    def is_empty(board: Board):
        for row in range(board.row):
            for col in range(board.col):
                if board[row, col].shape != ShapeConstant.BLANK:
                    return False
        return True

    @staticmethod
    def utility_function(board: Board, row: int, col: int):
        # yes i reused check_streak, no im not ashamed
        """
        [DESC] fungsi utk dapat value heuristik piece di board[row][col]
        [RETURN]
        0 if board[row][col] kosong
        int if ada isinya
        """
        piece = board[row, col]

        streak_way = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]
        mark = 0

        for prior in GameConstant.WIN_PRIOR:
            for row_ax, col_ax in streak_way:
                row_ = row + row_ax
                col_ = col + col_ax
                # since board is 6x7, 10 should be fine to check all cardinal directions
                for _ in range(10):
                    if is_out(board, row_, col_):
                        mark += 0
                        break
                    # true if shape different
                    shape_condition = (
                        prior == GameConstant.SHAPE
                        and piece.shape != board[row_, col_].shape
                    )
                    # true if color different
                    color_condition = (
                        prior == GameConstant.COLOR
                        and piece.color != board[row_, col_].color
                    )
                    # if meet blank piece
                    if board[row_, col_].shape == ShapeConstant.BLANK:
                        mark += 0
                    else:
                        # same color shape
                        if (not shape_condition) and (not color_condition):
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

    def select_random_move():
        pass

    def calculate_delta_e(current_state, current_value, random_neighbors):
        pass

    @staticmethod
    def hill_climbing(state: State, n_player: int, thinking_time: float):
        current_board = state.board
        mark = -999
        # default if all of the columns are empty (first move) prefer yg ditengah
        column_choice = current_board.col // 2
        for i in range(current_board.col):
            # cek dari atas ke bawah bcs kyk gini strukturnya
            for j in range(current_board.row - 1, -1, -1):
                # check for first piece thats not a blank in each column
                if current_board[j, i].shape != ShapeConstant.BLANK:
                    # top most row of current column is filled
                    if j == current_board.row - 1:
                        break
                current_mark = LocalSearch.utility_function(current_board, j - 1, i)
                if current_mark >= mark:  # change column choice
                    column_choice = i
                mark = max(current_mark, mark)
        return column_choice

    def simulated_annealing(self, current_state: State):
        # self.thinking_time = 3
        # self.max_depth = 5?
        # allocated_time = t + 0.6 / 7
        # Temperature = current time - allocated time
        allocated_time = self.thinking_time / (7 * self.max_depth) + time()
        current_value = LocalSearch.utility_function(current_state.board)
        available_moves = []

        # Iterate until the temperature is cool enough
        while True:
            # Check if the current time didnt exceed allocated time, temperature >= 0
            current_temperature = allocated_time - time()
            if current_temperature <= 0:
                return available_moves
            random_successor = self.select_random_move()
            if random_successor:
                delta_e = self.calculate_delta_e(
                    current_state, current_value, random_successor
                )
                if delta_e > 0:
                    available_moves.append(random_successor)
                else:
                    if exp(delta_e / current_temperature) > 0:
                        available_moves.append(random_successor)
