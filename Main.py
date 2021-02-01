import pprint as pp
from hoopers import *

if __name__ == "__main__":
    game = Hoopers()

    pp.pprint(game.valid_moves(coord=(1,5), count=0, hoop=False, valid_coords=[]))
    pp.pprint(game.valid_moves(coord=(5,1), count=0, hoop=False, valid_coords=[]))
    # pp.pprint(game.board)

    # print(game.board[-1][-1])
