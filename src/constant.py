import os


class ColorConstant:
    RED = "RED"
    BLUE = "BLUE"
    BLACK = "BLACK"


class ShapeConstant:
    CROSS = "X"
    CIRCLE = "O"
    BLANK = "-"


class GameConstant:
    SHAPE = "SHAPE"
    COLOR = "COLOR"
    WIN_PRIOR = [SHAPE, COLOR]
    PLAYER_COLOR = [ColorConstant.RED, ColorConstant.BLUE]
    N_COMPONENT_STREAK = 4

    PLAYER1_COLOR = ColorConstant.RED
    PLAYER1_SHAPE = ShapeConstant.CIRCLE
    PLAYER2_COLOR = ColorConstant.BLUE
    PLAYER2_SHAPE = ShapeConstant.CROSS

    BVB = 0  # Bot vs Bot
    PVB = 1  # Player vs Bot
    PVP = 2  # Player vs Player


class Path:
    PLAYER1 = 0
    PLAYER2 = 1
    FOLDER = "bin"
    BVB_FOLDER = "bvb"
    PVB_FOLDER = "pvb"
    BVB_P1 = os.path.join(FOLDER, BVB_FOLDER, "{}")
    BVB_P2 = os.path.join(FOLDER, BVB_FOLDER, "{}")
    PVB = os.path.join(FOLDER, PVB_FOLDER, "{}")