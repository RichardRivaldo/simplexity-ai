from src.ai import *
from src.constant import Path
from src.utility import dump


def dumper(path_b1, path_b2, path_pvb):
    model = Minimax7()
    dump(model, Path.BVB_P1.format(path_b1))
    dump(model, Path.BVB_P2.format(path_b2))
    dump(model, Path.PVB.format(path_pvb))


if __name__ == '__main__':
    bot1_filename = 'random-1.pkl'
    bot2_filename = 'random-2.pkl'
    pvp_bot_filename = 'random-1.pkl'
    dumper(bot1_filename, bot2_filename, pvp_bot_filename)
