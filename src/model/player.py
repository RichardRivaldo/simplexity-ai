class Player:
    """
    Class representation for Player

    [ATTRIBUTES]
        quota: dict -> piece shape quota owned by player
        shape: str -> shape representation for this player
        color: str -> color representation for this player
    """
    def __init__(self, shape: str, color: str, quota: dict):
        self.quota = quota
        self.shape = shape
        self.color = color

    def __eq__(self, other):
        return other.shape == self.shape and other.color == self.color
