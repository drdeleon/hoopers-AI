import pprint as pp
from hoopers import *

if __name__ == "__main__":
    game = Hoopers()

    game.board[0][0] = 3

    pp.pprint(game.board)

