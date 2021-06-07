from hoppers import *
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

    board_str += "    1  2  3  4  5  6  7  8  9  10 \n\n"

    for idx, row in enumerate(board):
        board_str += "%i  " % (idx + 1) if idx < 9 else "%i " % (idx + 1)
        for char in row:
            if char == 1:
                board_str += " W "
            elif char == 2:
                board_str += " B "
            elif char == 3:
                board_str += " * "
            else:
                board_str += " - "
        
        board_str += "\n"
    
    print(board_str)


def player_turn(curr_player:int, game:Hoppers):
    """ This is a player turn. """

    init_coord = input("Ingrese la coordenada de la pieza a mover (Ej. 1,2): ")
    init_coord = tuple(int(n) for n in init_coord.split(','))

    valid_moves = game.valid_moves(
        game.curr_node,
        init_coord,
        hoop=False,
        valid_dests=[]
    )

    print_board(game.get_state_board(game.curr_node.state), valid_moves)
    print("\nMovimientos válidos:", valid_moves)

    dest_coord = input("Ingrese la coordenada destino (Ej. 1,2): ")
    dest_coord = tuple(int(n) for n in dest_coord.split(','))

    return (init_coord, dest_coord)


def ai_turn(curr_player:int, game:Hoppers):
    """ This the AI turn. """

    print("AI procesando...")
    is_max = curr_player == 1

    start = time.time()

    if game.moves_count < 86 or 90 < game.moves_count:
        val, move = game.alpha_beta_search(
            node=game.curr_node,
            depth=2,
            max_player=is_max
        )

    else:
        val, move = game.alpha_beta_search(
            node=game.curr_node,
            depth=3,
            max_player=is_max
        )

    end = time.time()

    print("Tiempo ejecución AI: %.3fs" % float(end - start))

    return move[0], move[1]



if __name__ == "__main__":
    game = Hoppers(init_state=np.array([
        [
            (0,0), (0,1), (0,2), (0,3), (0,4),
            (1,0), (1,1), (1,2), (1,3), (2,0),
            (2,1), (2,2), (3,0), (3,1), (4,0)
        ],
        [
            (5,9), (6,9), (7,9), (8,9), (9,9),
            (6,8), (7,8), (8,8), (9,8), (7, 7),
            (8,7), (9,7), (8,6), (9,6), (9, 5)
        ]
    ]))

    print(MAIN_MENU)
    # game_mode = int(input("¿Qué modalidad quiere usar? "))
    game_mode = 4

    playing = True

    while playing:
        curr_player = 1 if game.player_one_turn else 2
        is_valid = False

        if game_mode == 1: # PvP
            while is_valid == False:
                print("\nTURNO JUGADOR", curr_player)

                print("\nTABLERO:")
                print_board(game.get_state_board(game.curr_node.state))

                if game.player_one_turn:
                    init, dest = player_turn(curr_player, game)
                    is_valid = game.move(init, dest)

                elif not game.player_one_turn:
                    init, dest = player_turn(curr_player, game)
                    is_valid = game.move(init, dest)


        elif game_mode == 2: # PvC
            while is_valid == False:
                print("\nTURNO JUGADOR", curr_player)

                print("\nTABLERO:")
                print_board(game.get_state_board(game.curr_node.state))

                if game.player_one_turn:
                    init, dest = player_turn(curr_player, game)
                    is_valid = game.move(init, dest)

                elif not game.player_one_turn:
                    init, dest = ai_turn(curr_player, game)
                    is_valid = game.move(init, dest)

        elif game_mode == 3: # CvP
            while is_valid == False:
                print("\nTURNO JUGADOR", curr_player)

                print("\nTABLERO:")
                print_board(game.get_state_board(game.curr_node.state))

                if game.player_one_turn:
                    init, dest = ai_turn(curr_player, game)
                    is_valid = game.move(init, dest)

                elif not game.player_one_turn:
                    init, dest = player_turn(curr_player, game)
                    is_valid = game.move(init, dest)

        elif game_mode == 4: # CvC
            while is_valid == False:
                print("\nTURNO JUGADOR", curr_player)

                print("\nTABLERO:")
                print_board(game.get_state_board(game.curr_node.state))

                if game.player_one_turn:
                    init, dest = ai_turn(curr_player, game)
                    is_valid = game.move(init, dest)

                elif not game.player_one_turn:
                    init, dest = ai_turn(curr_player, game)
                    is_valid = game.move(init, dest)


