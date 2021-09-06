from src.constant import ShapeConstant


class Config:
    """
    Class representation for configuration needed in game

    [ATTRIBUTES]
        row: int -> boards configuration row shape
        col: int -> boards configuration column shape
        game_type: int (Look at GameConstant for available type) -> game configuration for game type, 
            could be bot vs bot, player vs bot, and player vs player
        player_choice: int -> Could be 0 or 1 (only needed for player vs bot)
        thinking_time: float -> Maximal time for bot to think (only needed for player vs bot or bot vs bot)
        is_dump: bool -> is model loaded from bin file
    """

    def __init__(
        self,
        row: int,
        col: int,
        game_type: int,
        player_choice: int,
        is_dump: bool,
        thinking_time: float,
    ):
        self.row = row
        self.col = col
        self.is_dump = is_dump

        n_quota = row * col / 2
        self.quota = [
            {
                ShapeConstant.CROSS: n_quota // 2,
                ShapeConstant.CIRCLE: n_quota - (n_quota // 2),
            },
            {
                ShapeConstant.CROSS: n_quota - (n_quota // 2),
                ShapeConstant.CIRCLE: n_quota // 2,
            },
        ]

        self.game_type = game_type
        self.player_choice = player_choice  # 0 or 1
        if self.player_choice == None:
            self.player_choice = -1

        self.thinking_time = thinking_time

    def __str__(self):
        ret = '[Configuration]\n'
        ret += f'cow: {self.row}\n'
        ret += f'rol: {self.col}\n'
        ret += f'is_dump: {self.is_dump}\n'
        ret += f'game_type: {self.game_type}\n'
        ret += f'player_choice: {self.player_choice}\n'
        ret += f'thinking_time: {self.thinking_time}\n'
        return ret