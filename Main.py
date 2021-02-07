import pprint as pp
from hoopers import *

if __name__ == "__main__":
    game = Hoopers(init_state=(
            {
                (1,1), (1,2), (1,3), (1,4), (1,5),
                (2,1), (2,2), (2,3), (2,4), (3,1),
                (3,2), (3,3), (4,1), (4,2), (5, 1)
            },
            {
                (6,10), (7,10), (8,10), (9,10), (10,10),
                (7,9), (8,9), (9,9), (10,9), (8, 8),
                (9,8), (10,8), (9,7), (10,7), (10, 6)
            },
        ))

    pp.pprint(game.valid_moves(coord=(1,5), hoop=False, valid_dests=[]))
    pp.pprint(game.valid_moves(coord=(5,1), hoop=False, valid_dests=[]))
    pp.pprint(game.valid_moves(coord=(2,4), hoop=False, valid_dests=[]))
    # pp.pprint(game.board)

    print(game.is_valid_move((5,1), (5,3)))
    # print(game.board[-1][-1])

    pp.pprint(game.board)

    print(game.minimax(game.curr_node, 4, -math.inf, math.inf, True))
    pp.pprint(game.get_state_board(game.curr_node.state))