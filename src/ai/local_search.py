import random
from copy import deepcopy
from itertools import product
from math import exp
from time import time
from typing import List

from src.constant import ColorConstant
from src.utility import *


class LocalSearch7:
    def __init__(self, algorithm="HC"):
        self.algorithm = algorithm

    def find(
            self, state: State, n_player: int, thinking_time: float
    ) -> Tuple[int, str]:
        self.thinking_time = time() + thinking_time
        best_movement = self.local_search(state, n_player, self.algorithm)

        return best_movement

    @staticmethod
    def count_group_horizontal(board: Board, row: int, col: int):
        # return number of pieces in a 4 group horizontally
        count_piece = 0
        for i in range(col, col + 4):
            if (is_out(board, row, i)):
                return 0
            if board[row, i].shape != ShapeConstant.BLANK:
                count_piece += 1
        return count_piece

    @staticmethod
    def count_group_vertical(board: Board, row: int, col: int):
        # return number of pieces in a 4 group horizontally
        count_piece = 0
        for i in range(row, row + 4):
            if (is_out(board, i, col)):
                return 0
            if board[i, col].shape != ShapeConstant.BLANK:
                count_piece += 1
        return count_piece

    @staticmethod
    def count_group_diagonal(board: Board, row: int, col: int, direction: bool):
        # checks a group of 4 in board[row,col] returns number of pieces
        count_piece = 0
        if direction:  # check from left to right, dari atas ke bawah diagonal
            row_ = row
            col_ = col
            for i in range(4):
                if is_out(board, row_, col_):
                    return 0  # doesnt count if it went out
                if board[row_, col_].shape != ShapeConstant.BLANK:
                    count_piece += 1
                row_ = row_ + 1
                col_ = col_ + 1
        else:  # checks from right to left, dari atas ke bawah diagonal
            row_ = row
            col_ = col
            for i in range(4):
                if is_out(board, row_, col_):
                    return 0  # doesnt count if it went out
                if board[row_, col_].shape != ShapeConstant.BLANK:
                    count_piece += 1
                row_ = row_ - 1
                col_ = col_ + 1
        return count_piece

    @staticmethod
    def count_group_color_shape_horizontal(
            board: Board, color: ColorConstant, shape: ShapeConstant, row: int, col: int
    ):
        # return number of pieces in a group that fits either color or shape
        count_piece = 0
        for i in range(col, col + 4):
            if (is_out(board, row, i)):
                return 0
            if board[row, i].shape == shape or board[row, i].color == color:
                count_piece += 1
        return count_piece

    @staticmethod
    def count_group_color_shape_vertical(
            board: Board, color: ColorConstant, shape: ShapeConstant, row: int, col: int
    ):
        # return number of pieces in a group that fits either color or shape
        count_piece = 0
        for i in range(row, row + 4):
            if (is_out(board, i, col)):
                return 0
            if board[i, col].shape == shape or board[i, col].color == color:
                count_piece += 1
        return count_piece

    @staticmethod
    def count_group_color_shape_diagonal(
            board: Board, color: ColorConstant, shape: ShapeConstant, row: int, col: int, direction: bool
    ):
        # checks a group of 4 in board[row,col] returns number of pieces that fits either color or shape diagonally
        count_piece = 0
        if direction:  # check from left to right, dari atas ke bawah diagonal
            row_ = row
            col_ = col
            for i in range(4):
                if is_out(board, row_, col_):
                    return 0  # doesnt count if it went out
                if board[row_, col_].color == color or board[row_, col_].shape == shape:
                    count_piece += 1
                row_ = row_ + 1
                col_ = col_ + 1
        else:  # checks from right to left, dari atas ke bawah diagonal
            row_ = row
            col_ = col
            for i in range(4):
                if is_out(board, row_, col_):
                    return 0  # doesnt count if it went out
                if board[row_, col_].color == color or board[row_, col_].shape == shape:
                    count_piece += 1
                row_ = row_ - 1
                col_ = col_ + 1
        return count_piece

    @staticmethod
    def evaluate_group_horizontal(state: State, n_player: int, i: int, j: int):
        # return value of group 4 horizontally on position board[i,j]
        current_board = state.board
        my_player = state.players[n_player]
        enemy_player = state.players[
            (int(not n_player))
        ]  # not n_player since n_player can only be 1 or 0 will always refer to the other
        number_of_piece = LocalSearch7.count_group_horizontal(
            current_board, i, j)
        count_enemy_piece = LocalSearch7.count_group_color_shape_horizontal(
            current_board, enemy_player.color, enemy_player.shape, i, j
        )
        count_player_piece = LocalSearch7.count_group_color_shape_horizontal(
            current_board, my_player.color, my_player.shape, i, j
        )

        if number_of_piece == 4:
            # if 4 piece of a group are full
            if count_enemy_piece == 4:
                return -99999
            elif count_player_piece == 4:
                return 99999
            elif count_enemy_piece == 3:
                # 3 enemy and 1 us == enemy is blocked
                return 99999
            elif count_enemy_piece == 2:
                # 2 enemy and 2 us
                return 0
            else:  # 1 enemy and 3 us
                return 4
        elif number_of_piece == 3:
            # 3 pieces and 1 empty
            if count_enemy_piece == 3:
                # 3 enemies
                return -99999
            elif count_player_piece == 3:
                # 3 us
                return 10
            elif count_player_piece == 2:
                # 2 us 1 enemy
                return 4
            else:  # 1 us 2 enemy
                return -4
        elif number_of_piece == 2:
            # 2 pieces and 2 empty
            if count_enemy_piece == 2:
                return -4
            else:  # 1 enemy 1 us
                return 4
        elif number_of_piece == 1:
            # 1 pieces and 3 empty
            if count_enemy_piece == 1:
                return -1
            else:
                return +1
        # completely empty
        return 0

    @staticmethod
    def evaluate_group_vertical(state: State, n_player: int, i: int, j: int):
        current_board = state.board
        my_player = state.players[n_player]
        enemy_player = state.players[
            (int(not n_player))
        ]  # not n_player since n_player can only be 1 or 0 will always refer to the other
        number_of_piece = LocalSearch7.count_group_vertical(
            current_board, i, j)
        count_enemy_piece = LocalSearch7.count_group_color_shape_vertical(
            current_board, enemy_player.color, enemy_player.shape, i, j
        )
        count_player_piece = LocalSearch7.count_group_color_shape_vertical(
            current_board, my_player.color, my_player.shape, i, j
        )

        if number_of_piece == 4:
            # if 4 piece of a group are full
            if count_enemy_piece == 4:
                return -99999
            elif count_player_piece == 4:
                return 99999
            elif count_enemy_piece == 3:
                # 3 enemy and 1 us == enemy is blocked
                return 99999
            elif count_enemy_piece == 2:
                # 2 enemy and 2 us
                return 0
            else:  # 1 enemy and 3 us
                return 4
        elif number_of_piece == 3:
            # 3 pieces and 1 empty
            if count_enemy_piece == 3:
                # 3 enemies
                return -99999
            elif count_player_piece == 3:
                # 3 us
                return 10
            elif count_player_piece == 2:
                # 2 us 1 enemy
                return 4
            else:  # 1 us 2 enemy
                return -4
        elif number_of_piece == 2:
            # 2 pieces and 2 empty
            if count_enemy_piece == 2:
                return -4
            else:  # 1 enemy 1 us
                return 4
        elif number_of_piece == 1:
            # 1 pieces and 3 empty
            if count_enemy_piece == 1:
                return -1
            else:
                return +1
        # completely empty
        return 0

    @staticmethod
    def evaluate_group_diagonal(state: State, n_player: int, i: int, j: int, direction: bool):
        current_board = state.board
        my_player = state.players[n_player]
        enemy_player = state.players[
            (int(not n_player))
        ]  # not n_player since n_player can only be 1 or 0 will always refer to the other
        number_of_piece = LocalSearch7.count_group_diagonal(
            current_board, i, j, direction)
        count_enemy_piece = LocalSearch7.count_group_color_shape_diagonal(
            current_board, enemy_player.color, enemy_player.shape, i, j, direction
        )
        count_player_piece = LocalSearch7.count_group_color_shape_diagonal(
            current_board, my_player.color, my_player.shape, i, j, direction
        )
        if number_of_piece == 4:
            # if 4 piece of a group are full
            if count_enemy_piece == 4:
                return -99999
            elif count_player_piece == 4:
                return 99999
            elif count_enemy_piece == 3:
                # 3 enemy and 1 us == enemy is blocked
                return 99999
            elif count_enemy_piece == 2:
                # 2 enemy and 2 us
                return 0
            else:  # 1 enemy and 3 us
                return 4
        elif number_of_piece == 3:
            # 3 pieces and 1 empty
            if count_enemy_piece == 3:
                # 3 enemies
                return -99999
            elif count_player_piece == 3:
                # 3 us
                return 10
            elif count_player_piece == 2:
                # 2 us 1 enemy
                return 4
            else:  # 1 us 2 enemy
                return -4
        elif number_of_piece == 2:
            # 2 pieces and 2 empty
            if count_enemy_piece == 2:
                return -4
            else:  # 1 enemy 1 us
                return 4
        elif number_of_piece == 1:
            # 1 pieces and 3 empty
            if count_enemy_piece == 1:
                return -1
            else:
                return +1
        # completely empty
        return 0

    @staticmethod
    def state_heuristic(state: State, n_player: int):
        # function that returns a value of heuristic of a given state
        current_board = state.board

        state_value = 0
        # check horizontally 1 board
        for i in range(current_board.row):
            for j in range(0, current_board.col):
                state_value += LocalSearch7.evaluate_group_horizontal(
                    state, n_player, i, j
                )
        # check vertically 1 board
        for i in range(current_board.col):
            for j in range(0, current_board.row):
                state_value += LocalSearch7.evaluate_group_vertical(
                    state, n_player, j, i
                )

        # check diagonally
        for i in range(current_board.row):
            for j in range(current_board.col):
                state_value += LocalSearch7.evaluate_group_diagonal(
                    state, n_player, i, j, True
                )
                state_value += LocalSearch7.evaluate_group_diagonal(
                    state, n_player, i, j, False
                )
        # print(state_value)
        return state_value

    # Get empty column to place pieces
    @staticmethod
    def get_empty_column(current_state: State) -> List[int]:
        # Only need check if board[0] is empty (contains blank piece)
        current_board = current_state.board.board
        board_first_row = current_board[0]

        return [
            col
            for col in range(len(board_first_row))
            if board_first_row[col].shape == ShapeConstant.BLANK
        ]

    # Get pieces which shape is still available
    @staticmethod
    def get_available_shape(current_state: State, n_player: int) -> List[str]:
        current_player = current_state.players[n_player]
        current_player_quota = current_player.quota

        available_pieces = []
        for shape in current_player_quota:
            if current_player_quota[shape] > 0:
                available_pieces.append(shape)

        return available_pieces

    # Get all valid pairs of column and shape as valid moves
    def get_valid_moves(
            self, current_state: State, n_player: int
    ) -> List[Tuple[int, str]]:
        valid_columns = self.get_empty_column(current_state)
        valid_shape = self.get_available_shape(current_state, n_player)

        return list(product(valid_columns, valid_shape))

    # Select random move from valid moves
    def select_random_move(
            self, current_state: State, n_player: int
    ) -> Tuple[int, str]:
        valid_moves = self.get_valid_moves(current_state, n_player)
        return random.choice(valid_moves)

    @staticmethod
    def make_dummy_move(current_state: State, n_player: int, shape: str, col: int):
        neighbor_state = deepcopy(current_state)
        piece = Piece(shape, GameConstant.PLAYER_COLOR[n_player])
        for row in range(neighbor_state.board.row - 1, -1, -1):
            if neighbor_state.board[row, col].shape == ShapeConstant.BLANK:
                neighbor_state.board.set_piece(row, col, piece)
                return neighbor_state

    # Calculate delta e, difference of current and next state value
    def calculate_delta_e(
            self,
            current_state: State,
            current_value: int,
            random_successor: Tuple[int, str],
            n_player: int,
    ):
        # Copy dummy state and apply dummy move to calculate delta E without breaking current state
        neighbor_state = LocalSearch7.make_dummy_move(
            current_state, n_player, random_successor[1], random_successor[0])
        neighbor_value = self.state_heuristic(neighbor_state, n_player)

        return neighbor_value - current_value

    # Hill Climbing: Sideways Move Variant with modifications
    # The algorithm is fast enough for thinking time of 3 seconds
    def hill_climbing(self, current_state: State, n_player: int) -> Tuple[int, str]:
        # Container for all move evaluation and list of valid moves
        valid_moves = self.get_valid_moves(current_state, n_player)
        move_evaluations = []

        # Iterate while current time doesn't exceed thinking time
        for valid_move in valid_moves:
            # Evaluate each valid moves' value by applying dummy move to neighbor state
            neighbor_state = LocalSearch7.make_dummy_move(
                current_state, n_player, valid_move[1], valid_move[0])
            print(self.state_heuristic(neighbor_state, n_player))
            neighbor_value = self.state_heuristic(neighbor_state, n_player)
            move_evaluations.append([valid_move, neighbor_value])

        # Always return move with maximum values, doesn't matter if it's < current value
        # Automatically do sideways move if the maximum value is = current value
        if move_evaluations:
            return max(move_evaluations, key=lambda x: x[1])[0]
        else:
            return self.select_random_move(current_state, n_player)

    # Local search method using Simulated Annealing with modifications
    def simulated_annealing(self, current_state: State, n_player: int) -> Tuple[int, str]:
        # self.thinking_time = t + 3
        # allocated_time = t + 3 -> Takes all the thinking time
        allocated_time = self.thinking_time
        # Calculate the current state value
        current_value = self.state_heuristic(current_state, n_player)

        # Greedy Simulated Annealing -> Find best neighbor that gives highest state value
        # Initialize value for comparison
        move_choice = (None, None)
        move_value = 0
        move_probability = random.uniform(0, 1)

        # Iterate until the temperature is cool enough
        while True:
            # Current temperature = current time - allocated time
            # Check if the current time didn't exceed allocated time, temperature >= 0
            current_temperature = allocated_time - time()
            if current_temperature <= 10e-4:
                # If there are move choices, select the one with maximum differences with current state
                # Else select a random valid move
                if move_choice:
                    return move_choice
                else:
                    return self.select_random_move(current_state, n_player)

            # Generate random move and check the difference on state value
            random_next_move = self.select_random_move(current_state, n_player)
            print(str(random_next_move[0]) + "kolom")
            if random_next_move:
                delta_e = self.calculate_delta_e(
                    current_state, current_value, random_next_move, n_player)
                if delta_e > 0:
                    if delta_e > move_value:
                        move_choice = random_next_move
                        move_value = self.state_heuristic(self.make_dummy_move(
                            current_state, n_player, random_next_move[1], random_next_move[0]), n_player)
                elif exp(delta_e / current_temperature) > move_probability:
                    move_choice = random_next_move
                    move_value = self.state_heuristic(self.make_dummy_move(
                        current_state, n_player, random_next_move[1], random_next_move[0]), n_player)

    # Wrapper to find best move based on algorithm choice
    def local_search(self, current_state: State, n_player: int, algorithm: str) -> Tuple[int, str]:
        if algorithm == "SA":
            return self.simulated_annealing(current_state, n_player)
        elif algorithm == "HC":
            return self.hill_climbing(current_state, n_player)
        else:
            raise ValueError("No mentioned algorithm implementation")
