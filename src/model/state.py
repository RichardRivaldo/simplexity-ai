from src.model.board import Board
from src.model.player import Player

from typing import List


class State:
    """
    Class representation for State every turn

    [ATTRIBUTES]
        board: Board -> current board in this state
        players: List[Player] -> list of players in game
        round: int -> Current round
    """
    def __init__(self, board: Board, players: List[Player], round: int):
        self.board = board
        self.players = players
        self.round = round
