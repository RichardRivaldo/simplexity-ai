import copy
from os import stat
import random
from time import time

from src.constant import ShapeConstant, GameConstant
from src.model import State, Board, Player, Piece
from itertools import product

from typing import Tuple, List


class Minimax:
    ON_PROGRESS = "ON_PROGRESS"
    DRAW = "DRAW"
    WIN = "WIN"
    LOSE = "LOSE"

    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        # best_movement = (random.randint(0, state.board.col - 1), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        # start_time = time()        
        best_movement = Minimax.MinimaxAlphaBetaPruning(state, -9999, 9999, True, n_player, time() + thinking_time)[1] # minimax algorithm

        # neighbor_state = copy.deepcopy(state)
        # try_place = Minimax.place(neighbor_state, n_player, best_movement[1], best_movement[0])

        # print("--------------")
        # if try_place != -1:            
        #     outcome = Minimax.get_current_outcome(neighbor_state, n_player)
        #     print(outcome)
        #     print(Minimax.is_game_over(outcome))
        #     print(Minimax.utility_function(neighbor_state, outcome))
        # else:
        #     print("INVALID")
        
        print("move ---------------------")
        print(best_movement)
        return best_movement


    def utility_function(state: State, outcome: str):
        fill_count = 0
        for row in range(state.board.row):
            for col in range(state.board.col):
                if state.board[row, col].shape != ShapeConstant.BLANK:
                    fill_count += 1
                    
        value = 42 - fill_count + 1
        
        if outcome == Minimax.WIN:
            return value

        if outcome == Minimax.LOSE:
            return -1 * value

        return 0        

    '''
            if (state = gameOver){  #kondisi menang, seri, kalah
            return UtilityFunction(state)
        }
        if (whitePlayer -> kalo giliran kita) {	# White Player, find the maximum
            maxValue ← (- infinity)
            tempState := None
            For each child of state{
            # tempState = child
            tempValue ←  minimaxBot(child, alpha, beta, False)
            maxValue ←  max(tempValue, maxValue)
            alpha ← max (alpha, maxValue)
            If (beta ≤ alpha){
            Break 	 #prune this child and all child of this child
        }
        }
            return maxValue, 
        }
        else { -> kalo giliran musuh		# Black Player, find the minimum
            minValue ← (+ infinity)
            For each child of state{
            tempValue ←  minimaxBot(child, alpha, beta, True)
            maxValue ←  min(tempValue, minValue)
        beta ← min (beta, minValue)
            if (beta ≤ alpha){
            Break 	 #prune this child and all child of this child
        }
        }
            return minValue
        }
        }

    '''
    # kalau kita main sebagai player 1 (n_player = 0) maka white_player true, vice versa
    # White -> memaksimumkan
    # Black -> meminimumkan

    # if (n_player == 0):
    #     MinimaxAlphaBetaPruning(state, alpha, beta, True, 0)
    # else:
    #     MinimaxAlphaBetaPruning(state, alpha, beta, False, 1)
    @staticmethod
    def MinimaxAlphaBetaPruning(state: State, alpha: int, beta: int, white_player: bool, n_player: int, thinking_time: float) -> Tuple[int, Tuple[int, str]]:
        current_board = state.board
        
        outcome = Minimax.get_current_outcome(state, n_player)
        # print(state.board)
        if Minimax.is_game_over(outcome):
            # print(Minimax.utility_function(state, outcome))
            # test = input("Ujung gan")
            return (Minimax.utility_function(state, outcome), ())

        if white_player:
            maxVal = -9999 # negative infinity
            
            valid_moves = Minimax.get_valid_moves(state, n_player)
            random.shuffle(valid_moves)
            maxMove = None
            
            # For each child of current state
            for move in valid_moves:
                if (time()) > thinking_time:
                    print("HEHE")
                    return (maxVal, random.choice(valid_moves) if maxMove == None else maxMove)
                neighbor_state = copy.deepcopy(state)
                try_place = Minimax.place(neighbor_state, n_player, move[1], move[0])
                
                tempResult = Minimax.MinimaxAlphaBetaPruning(neighbor_state, alpha, beta, not white_player, n_player, thinking_time)
                tempValue = tempResult[0]
                
                if (tempValue > maxVal):
                    maxVal = tempValue
                    maxMove = move

                alpha = max(alpha, maxVal)

                if (beta <= alpha):
                    # test = input("test: di white")
                    break
            
            return (maxVal, maxMove)
            
        else:
            minVal = 9999 # positive infinity
            
            black_n_player = n_player ^ 1
            valid_moves = Minimax.get_valid_moves(state, black_n_player)
            random.shuffle(valid_moves)
            minMove = None 
            
            for move in valid_moves:
                if (time()) > thinking_time:
                    print("HEHE")
                    return (minVal, random.choice(valid_moves) if minMove == None else minMove)
                neighbor_state = copy.deepcopy(state)
                Minimax.place(neighbor_state, black_n_player, move[1], move[0])
                tempResult = Minimax.MinimaxAlphaBetaPruning(neighbor_state, alpha, beta, not white_player, n_player, thinking_time)
                tempValue = tempResult[0]

                if tempValue < minVal:
                    minVal = tempValue
                    minMove = move
                
                beta = min(beta, minVal)
                
                if (beta <= alpha):
                    # test = input("test: di black")
                    break
                
            return (minVal, minMove)                                        


    @staticmethod
    def is_win(board: Board) -> str:
        """
        [DESC]
            Function to check if player won
        [PARAMS]
            board: Board -> current board
        [RETURN]
            None if there is no streak
            Tuple[shape, color] match with player set if there is a streak
        """
        temp_win = None
        for row in range(board.row):
            for col in range(board.col):
                checked = Minimax.check_streak(board, row, col)
                if checked:
                    if checked[0] == GameConstant.WIN_PRIOR[0]:
                        return checked[1]
                    else:
                        temp_win = checked[1]

        return temp_win

    def get_current_outcome(state: State, n_player: int) -> str:
        temp_win = Minimax.is_win(state.board)
        if temp_win == None:
            return Minimax.DRAW if Minimax.is_full(state.board) else Minimax.ON_PROGRESS

        for i, player in enumerate(state.players):
            if temp_win[0] == player.shape and temp_win[1] == player.color:
                if i == n_player:
                    return Minimax.WIN
                else:
                    return Minimax.LOSE

    def is_game_over(outcome: str) -> bool:
        GAME_OVER_OUTCOMES = [Minimax.WIN, Minimax.LOSE, Minimax.DRAW]

        return outcome in GAME_OVER_OUTCOMES

    @staticmethod
    def check_streak(board: Board, row: int, col: int) -> Tuple[str, str, str]:
        """
        [DESC]
            Function to check streak from row, col in current board
        [PARAMS]
            board: Board -> current board
            row: int -> row
            col: int -> column
        [RETURN]
            None if the row, col in a board isn't filled with piece
            Tuple[prior, shape, color] match with player set if streak found and cause of win
        """
        piece = board[row, col]
        if piece.shape == ShapeConstant.BLANK:
            return None

        streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for prior in GameConstant.WIN_PRIOR:
            mark = 0
            for row_ax, col_ax in streak_way:
                row_ = row + row_ax
                col_ = col + col_ax
                for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                    if Minimax.is_out(board, row_, col_):
                        mark = 0
                        break

                    shape_condition = (
                        prior == GameConstant.SHAPE
                        and piece.shape != board[row_, col_].shape
                    )
                    color_condition = (
                        prior == GameConstant.COLOR
                        and piece.color != board[row_, col_].color
                    )
                    if shape_condition or color_condition:
                        mark = 0
                        break

                    row_ += row_ax
                    col_ += col_ax
                    mark += 1

                if mark == GameConstant.N_COMPONENT_STREAK - 1:
                    player_set = [
                        (GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR),
                        (GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR),
                    ]
                    for player in player_set:
                        if prior == GameConstant.SHAPE:
                            if piece.shape == player[0]:
                                return (prior, player)
                                
                        elif prior == GameConstant.COLOR:
                            if piece.color == player[1]:
                                return (prior, player)

    @staticmethod
    def is_out(board: Board, row: int, col: int) -> bool:
        """
        [DESC]
            Function to see if the piece (row, col) is outside of the board
        [PARAMS]
            board: Board -> current board
            row: int -> row to be checked
            col: int -> column to be checked
        [RETURN]
            True if outside board
            False if inside board
        """
        return row < 0 or row >= board.row or col < 0 or col >= board.col

    @staticmethod
    def is_full(board: Board) -> bool:
        """
        [DESC]
            Function to see if current board is full of pieces
        [PARAMS]
            board: Board -> current board
        [RETURN]
            True if board is full
            False if board is not full
        """
        for row in range(board.row):
            for col in range(board.col):
                if board[row, col].shape == ShapeConstant.BLANK:
                    return False
        return True

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
            current_state: State, n_player: int
    ) -> List[Tuple[int, str]]:
        valid_columns = Minimax.get_empty_column(current_state)
        valid_shape = Minimax.get_available_shape(current_state, n_player)

        return list(product(valid_columns, valid_shape))




