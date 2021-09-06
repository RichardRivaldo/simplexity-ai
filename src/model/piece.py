from clint.textui import colored

from src.constant import ColorConstant


class Piece:
    """
    Class representation for Piece inside Board

    [ATTRIBUTES]
        shape: str -> Shape piece inside board
        color: str -> Color piece inside board
    """

    def __init__(self, shape: str, color: str):
        self.shape = shape
        self.color = color

    def __str__(self):
        if self.color == ColorConstant.RED:
            return colored.red(self.shape)
        elif self.color == ColorConstant.BLUE:
            return colored.blue(self.shape)
        elif self.color == ColorConstant.BLACK:
            return colored.green(self.shape)

    def __eq__(self, o: object) -> bool:
        return self.shape == o.shape and self.color == o.color
