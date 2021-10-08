import copy
import random
from itertools import product
from math import exp
from time import time
from typing import List, Tuple

from src.constant import ColorConstant, ShapeConstant, GameConstant
from src.model import Board, State, Player, Piece
from src.utility import place


class LocalSearch:
    def __init__(self):
        pass

    def find(
            self, state: State, n_player: int, thinking_time: float
    ) -> Tuple[int, str]:
        self.thinking_time = time() + thinking_time
        best_movement = self.find_best_move(state, n_player)

        return best_movement

    @staticmethod
    def count_group_horizontal(board: Board, row: int, col: int):
        # return number of pieces in a 4 group horizontally
        count_piece = 0
        for i in range(col, col + 4):
            if board[row, i].shape != ShapeConstant.BLANK:
                count_piece += 1
        return count_piece

    @staticmethod
    def count_group_vertical(board: Board, row: int, col: int):
        # return number of pieces in a 4 group horizontally
        count_piece = 0
        for i in range(row, row + 4):
            if board[i, col].shape != ShapeConstant.BLANK:
                count_piece += 1
        return count_piece

    @staticmethod
    def count_group_color_shape_horizontal(
            board: Board, color: ColorConstant, shape: ShapeConstant, row: int, col: int
    ):
        # return number of pieces in a group that fits either color or shape
        count_piece = 0
        for i in range(col, col + 4):
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
            if board[i, col].shape == shape or board[i, col].color == color:
                count_piece += 1
        return count_piece

    @staticmethod
    def evaluate_group_horizontal(state: State, n_player: int, i: int, j: int):
        # return value of group 4 horizontally on position board[i,j]
        current_board = state.board
        my_player = state.players[n_player]
        enemy_player = state.players[
            (int(not n_player))
        ]  # not n_player since n_player can only be 1 or 0 will always refer to the other
        number_of_piece = LocalSearch.count_group_horizontal(
            current_board, i, j)
        count_enemy_piece = LocalSearch.count_group_color_shape_horizontal(
            current_board, enemy_player.color, enemy_player.shape, i, j
        )
        count_player_piece = LocalSearch.count_group_color_shape_horizontal(
            current_board, my_player.color, my_player.shape, i, j
        )

        if number_of_piece == 4:
            # if 4 piece of a group are full
            if count_enemy_piece == 4:
                return -99999
            elif count_player_piece == 4:
                return 999
            elif count_enemy_piece == 3:
                # 3 enemy and 1 us == enemy is blocked
                return 999
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
        number_of_piece = LocalSearch.count_group_vertical(current_board, i, j)
        count_enemy_piece = LocalSearch.count_group_color_shape_vertical(
            current_board, enemy_player.color, enemy_player.shape, i, j
        )
        count_player_piece = LocalSearch.count_group_color_shape_vertical(
            current_board, my_player.color, my_player.shape, i, j
        )

        if number_of_piece == 4:
            # if 4 piece of a group are full
            if count_enemy_piece == 4:
                return -99999
            elif count_player_piece == 4:
                return 999
            elif count_enemy_piece == 3:
                # 3 enemy and 1 us == enemy is blocked
                return 999
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
            for j in range(0, current_board.col - 4):
                state_value += LocalSearch.evaluate_group_horizontal(
                    state, n_player, i, j
                )
        # check vertically 1 board
        for i in range(current_board.col):
            for j in range(0, current_board.row - 4):
                state_value += LocalSearch.evaluate_group_vertical(
                    state, n_player, j, i
                )

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
    def hill_climbing(state: State, n_player: int):
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
                current_mark = LocalSearch.utility_function(
                    current_board, j - 1, i)
                if current_mark >= mark:  # change column choice
                    column_choice = i
                mark = max(current_mark, mark)
        return column_choice

    @staticmethod
    def place(state: State, n_player: int, shape: str, col: int) -> int:
        """
        [DESC]
            Function to place piece in board
        [PARAMS]
            state = current state in the game
            n_player = which player (player 1 or 2)
            shape = shape
            col = which col
        [RETURN]
            -1 if placement is invalid
            int(row) if placement is valid 
        """
        if state.players[n_player].quota[shape] == 0:
            return -1

        for row in range(state.board.row - 1, -1, -1):
            if state.board[row, col].shape == ShapeConstant.BLANK:
                piece = Piece(shape, GameConstant.PLAYER_COLOR[n_player])
                state.board.set_piece(row, col, piece)
                state.players[n_player].quota[shape] -= 1
                return row

        return -1

    # Calculate delta e, difference of current and next state value
    def calculate_delta_e(
            self,
            current_state: State,
            current_value: int,
            random_successor: Tuple[int, str],
            n_player: int,
    ):
        # Copy dummy state and apply move to calculate delta E without breaking current state
        neighbor_state = copy.deepcopy(current_state)
        try_place = LocalSearch.place(  # function di utility gabisa
            neighbor_state, n_player, random_successor[1],
            random_successor[0]
        )
        if try_place != -1:
            neighbor_value = self.state_heuristic(neighbor_state, n_player)

        return neighbor_value - current_value

    # Local search method using Simulated Annealing with modifications
    def simulated_annealing(self, current_state: State, n_player: int) -> Tuple[int, str]:
        # self.thinking_time = t + 3
        # allocated_time = t + 3 -> Takes all the thinking time
        allocated_time = self.thinking_time
        # Calculate the current state value
        current_value = self.state_heuristic(current_state, n_player)

        # Greedy Simulated Annealing -> Find best neighbor that gives highest state value
        move_choices = []

        # Iterate until the temperature is cool enough
        while True:
            # Current temperature = current time - allocated time
            # Check if the current time didn't exceed allocated time, temperature >= 0
            current_temperature = allocated_time - time()
            if current_temperature <= 0:
                # If there are move choices, select the one with maximum differences with current state
                # Else select a random valid move
                if move_choices:
                    return max(move_choices, key=lambda x: x[1])[0]
                else:
                    return self.select_random_move(current_state, n_player)

            # Generate random move and check the difference on state value
            random_next_move = self.select_random_move(current_state, n_player)
            if random_next_move:
                delta_e = self.calculate_delta_e(
                    current_state, current_value, random_next_move, n_player)
                if delta_e > 0 or exp(delta_e / current_temperature) > random.uniform(0, 1):
                    move_choices.append([random_next_move, delta_e])

    # Wrapper to find best move based on algorithm choice
    def find_best_move(self, current_state: State, n_player: int, algorithm="SA") -> Tuple[int, str]:
        if algorithm == "SA":
            return self.simulated_annealing(current_state, n_player)
        elif algorithm == "HC":
            return self.hill_climbing(current_state, n_player)
        else:
            raise ValueError("No mentioned algorithm implementation")
