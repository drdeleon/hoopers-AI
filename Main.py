import pprint as pp
from hoopers import *

if __name__ == "__main__":
    game = Hoopers()

    pp.pprint(game.valid_moves(coord=(1,5), hoop=False, valid_coords=[]))
    pp.pprint(game.valid_moves(coord=(5,1), hoop=False, valid_coords=[]))
    # pp.pprint(game.board)

    print(game.is_valid_move((5,1), (5,3)))
    # print(game.board[-1][-1])
