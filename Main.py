from hoppers import *
import pprint as pp
import time


MAIN_MENU = """
    MENÚ PRINCIPAL
    --------------
    1. PvP
    2. PvC
    3. CvP
    4. CvC
"""

def print_board(board, valid_moves=None):
    """ Print board with all possible moves. """

    board_str = ""
    if valid_moves != None:
        for pair in valid_moves:
            board[pair[0]-1][pair[1]-1] = 3

    board_str += "     1    2    3    4    5    6    7    8    9    10 \n"

    for idx, row in enumerate(board):
        board_str += "    ___  ___  ___  ___  ___  ___  ___  ___  ___  ___\n"
        board_str += "%i  " % (idx + 1) if idx < 9 else "%i " % (idx + 1)
        for char in row:
            if char == 1:
                board_str += "|_W_|"
            elif char == 2:
                board_str += "|_B_|"
            elif char == 3:
                board_str += "|_*_|"
            else:
                board_str += "|___|"
        
        board_str += "\n"
    
    print(board_str)


def player_turn(curr_player:int, game:Hoppers):
    """ This is a player turn. """

    print("\nPLAYER", curr_player, "TURN")

    print("\nTABLERO:")
    print_board(game.get_state_board(game.curr_node.state))

    init_coord = input("Ingrese la coordenada de la pieza a mover (Ej. 1,2): ")
    init_coord = tuple(int(n) for n in init_coord.split(','))

    valid_moves = game.valid_moves(
        game.curr_node,
        init_coord,
        hoop=False,
        valid_dests=[]
    )

    print("\nTABLERO:")
    print_board(game.get_state_board(game.curr_node.state), valid_moves)
    print("\nMovimientos válidos:", valid_moves)

    dest_coord = input("Ingrese la coordenada destino (Ej. 1,2): ")
    dest_coord = tuple(int(n) for n in dest_coord.split(','))


def ai_turn(curr_player:int, game:Hoppers):
    """ This the AI turn. """

    start = time.time()

    val, move = game.minimax(
        node=game.curr_node,
        depth=3,
        alpha=-math.inf,
        beta=math.inf,
        max_player=True
    )

    end = time.time()
    
    print("Tiempo ejecución AI: %.3fs" % float(end - start))



if __name__ == "__main__":
    game = Hoppers(init_state=np.array([
        [
            (1,1), (1,2), (1,3), (1,4), (1,5),
            (2,1), (2,2), (2,3), (2,4), (3,1),
            (3,2), (3,3), (4,1), (4,2), (5, 1)
        ],
        [
            (6,10), (7,10), (8,10), (9,10), (10,10),
            (7,9), (8,9), (9,9), (10,9), (8, 8),
            (9,8), (10,8), (9,7), (10,7), (10, 6)
        ]
    ]))

    print(MAIN_MENU)
    game_mode = int(input("¿Qué modalidad quiere usar?"))

    playing = True

    while playing:
        curr_player = 1 if game.player_one_turn else 2

        if game.player_one_turn: # P1's turn
            is_valid = False
            while not is_valid:
                try:
                    print("\nPLAYER", curr_player, "TURN")

                    print("\nTABLERO:")
                    print_board(game.get_state_board(game.curr_node.state))

                    init_coord = input("Ingrese la coordenada de la pieza a mover (Ej. 1,2): ")
                    init_coord = tuple(int(n) for n in init_coord.split(','))

                    valid_moves = game.valid_moves(
                        game.curr_node,
                        init_coord,
                        hoop=False,
                        valid_dests=[]
                    )

                    print("\nTABLERO:")
                    print_board(game.get_state_board(game.curr_node.state), valid_moves)
                    print("\nMovimientos válidos:", valid_moves)

                    dest_coord = input("Ingrese la coordenada destino (Ej. 1,2): ")
                    dest_coord = tuple(int(n) for n in dest_coord.split(','))
                    
                    # Movemos la pieza
                    is_valid = game.move(init_coord, dest_coord)

                except Exception:
                    print("¡Ingresar coordenada válida!"\
                        "La coordenada no es válida.")
        
        elif not game.player_one_turn: # P1's turn

            start = time.time()

            val, move = game.minimax(
                node=game.curr_node,
                depth=3,
                alpha=-math.inf,
                beta=math.inf,
                max_player=True
            )

            end = time.time()
            print("Tiempo ejecución AI: %.3fs" % float(end - start))

            print("AI movío de ", move[0], "a", move[1])

            is_valid = game.move(move[0], move[1])


