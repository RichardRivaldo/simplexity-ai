import pickle
from typing import Tuple

from src.model import Piece, Board, State
from src.constant import ShapeConstant, GameConstant


def dump(obj, path):
    """
    [DESC]
        Function to dump Object
    [PARAMS]
        obj: Object -> objects you want dump 
    """
    pickle.dump(obj, open(path, "wb"))


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
                if is_out(board, row_, col_):
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


def is_win(board: Board) -> Tuple[str, str]:
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
            checked = check_streak(board, row, col)
            if checked:
                if checked[0] == GameConstant.WIN_PRIOR[0]:
                    return checked[1]
                else:
                    temp_win = checked[1]
    return temp_win


def place(state: State, n_player: int, shape: str, col: str) -> int:
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
