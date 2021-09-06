import pickle
from time import time

from src.ai import Minimax
from src.model import Board, Player, State, Config
from src.constant import ShapeConstant, GameConstant, Path
from src.utility import is_out, is_win, is_full, place


class Game:
    """
    Class represetation for Main Game

    [ATTRIBUTES]
        config: Config -> configuration used for gameplay
        state: State -> current state in a round
        bot: List[Bot] -> bot used in pvb or bvb

    [METHODS]
        __gen_player -> Generate player, if is_dump == True, 
            it will take bot from bin folder based on game type in config 
        __input -> Input for player
        __is_valid -> Check if input is valid
        __placement -> Placement phase for player or bot
    """
    def __init__(self, config: Config):
        print(config)
        self.config = config

        board = Board(config.row, config.col)
        players = [
            Player(
                GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR, config.quota[0]
            ),
            Player(
                GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR, config.quota[1]
            ),
        ]

        self.__gen_player()
        self.state = State(board, players, 1)

    def __gen_player(self):
        if self.config.game_type == GameConstant.BVB:
            if not self.config.is_dump:
                # You can change model used here
                model1 = Minimax()
                model2 = Minimax()
            else:
                # Don't change this
                model1 = pickle.load(open(Path.BVB_P1, "rb"))
                model2 = pickle.load(open(Path.BVB_P2, "rb"))

            self.bot = [model1, model2]

        elif self.config.game_type == GameConstant.PVB:
            if not self.config.is_dump:
                # You can change model used here
                model = Minimax()
            else:
                # Don't change this
                model = pickle.load(open(Path.PVB, "rb"))

            if self.config.player_choice == 0:
                self.bot = [None, model]
            else:
                self.bot = [model, None]
        else:
            self.bot = []

    def __input(self):
        choosen_col = int(input("Put Column: "))
        choosen_shape = str(input("Put Shape: "))
        return choosen_col, choosen_shape

    def __is_valid(self, choosen_col, choosen_shape):
        if not is_out(self.state.board, 0, choosen_col) and choosen_shape in [ShapeConstant.CROSS, ShapeConstant.CIRCLE]:
            return True
        return False

    def __placement(self, player):
        player_turn = (self.state.round - 1) % 2

        while True:
            if self.config.game_type == GameConstant.PVB:
                if player_turn == self.config.player_choice:
                    choosen_col, choosen_shape = self.__input()
                else:
                    start = time()
                    choosen_col, choosen_shape = self.bot[player_turn].find(
                        self.state, player_turn, self.config.thinking_time
                    )
                    print(f'Runtime: {time() - start}')

            elif self.config.game_type == GameConstant.PVP:
                choosen_col, choosen_shape = self.__input()

            else:  # BVB
                start = time()
                choosen_col, choosen_shape = self.bot[player_turn].find(
                    self.state, player_turn, self.config.thinking_time
                )
                print(f'Runtime: {time() - start}')

            
            if self.__is_valid(choosen_col, choosen_shape):
                break

            print(f"{choosen_col} {choosen_shape} input are not valid")

        placement = place(self.state, player, choosen_shape, choosen_col)
        return placement

    def gameplay(self):
        while True:
            player = (self.state.round - 1) % 2
            print(f"Round {self.state.round}")
            print(self.state.board)
            print("\nShape Quota")
            for k, v in self.state.players[player].quota.items():
                print(f'\tShape "{k}": {v}')
            placement = self.__placement(player)

            while placement == -1:
                print(self.state.board)
                placement = self.__placement(player)

            self.state.round += 1
            winner = is_win(self.state.board)
            if winner:
                print(self.state.board)
                break
            if is_full(self.state.board):
                break

        if winner:
            for i, player in enumerate(self.state.players):
                if winner[0] == player.shape and winner[1] == player.color:
                    print(
                        f"Player {i + 1} with color {player.color} and shape {player.shape} Win"
                    )
                    break
        else:
            print("DRAW")
