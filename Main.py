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

    playing = True

    while playing:
        player_turn = 1 if game.is_p1_turn else 2
        print("\nTABLERO:")
        pp.pprint(game.get_state_board(game.curr_node.state))

        print("PLAYER ", player_turn, "TURN")

        if player_turn == 2:
            is_valid = False
            while not is_valid:
                try:
                    init_coord = input("Ingrese la coordenada de la pieza a mover: ")
                    init_coord = tuple(int(n) for n in init_coord.split(','))
                    print("Movimientos válidos:", game.valid_moves(game.curr_node, init_coord, hoop=False, valid_dests=[]))

                    dest_coord = input("Ingrese la coordenada destino: ")
                    dest_coord = tuple(int(n) for n in dest_coord.split(','))
                    
                    is_valid = game.move(init_coord, dest_coord) # Movemos la pieza

                except Exception:
                    print("¡Ingresar coordenada válida!")
        
        elif player_turn == 1:
            val, move = game.minimax(game.curr_node, 3, -math.inf, math.inf, True)
            print("AI movío de ", move[0], "a", move[1])

            is_valid = game.move(move[0], move[1])
               


    # pp.pprint(game.board)

    # print(game.minimax(game.curr_node, 4, -math.inf, math.inf, False))

    # pp.pprint(game.get_state_board(game.curr_node.state))