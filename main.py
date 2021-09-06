import argparse

from src.model import Config
from src.constant import GameConstant, Path
from src.mechanic import Game

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--row", required=True, help="num row board")
    parser.add_argument("-c", "--column", required=True, help="num column board")
    parser.add_argument(
        "-t",
        "--type",
        required=True,
        help="pvp for Player vs Player, pvb for Player vs Bot, bvb for Bot vs Bot",
    )
    parser.add_argument(
        "-pc",
        "--player_choice",
        required=False,
        help="choice player turn if you play human vs bot. Choose 0 or 1",
    )
    parser.add_argument(
        "-tt", "--thinking_time", required=True, help="max bot for thinking"
    )
    parser.add_argument(
        "-d",
        "--is_dump",
        action="store_true",
        required=False,
        help="max bot for thinking",
    )
    parser.add_argument("-b1", "--bot1", required=False, help="filename for bot 1 for pvb or bvb player 1")
    parser.add_argument("-b2", "--bot2", required=False, help="filename for bot 2 for bvb player 2")

    args = parser.parse_args()

    row = int(args.row)
    col = int(args.column)
    is_dump = args.is_dump

    if (row * col) % 2 != 0:
        raise Exception("Row times Col is not even")

    raw_type = args.type

    if raw_type == "bvb":
        type = GameConstant.BVB
        player_choice = None
        bot1 = args.bot1
        bot2 = args.bot2
        Path.BVB_P1 = Path.BVB_P1.format(bot1)
        Path.BVB_P2 = Path.BVB_P2.format(bot2)

    elif raw_type == "pvb":
        type = GameConstant.PVB
        player_choice = int(args.player_choice)
        bot_path = args.bot1
        if player_choice < 0 or player_choice > 1:
            raise Exception("Please Input 0 or 1 for --player_choice")
        Path.PVB = Path.PVB.format(bot_path)
        

    elif raw_type == "pvp":
        type = GameConstant.PVP
        player_choice = None

    else:
        raise Exception("Please Input bvb, pvb, or pvp for --type")

    thinking_time = float(args.thinking_time)
    config = Config(row, col, type, player_choice, is_dump, thinking_time)
    game = Game(config)
    game.gameplay()
