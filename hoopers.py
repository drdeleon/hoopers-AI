import pprint as pp


class Hoopers(object):
    """ Hoopers game class. Contains game state and methods. """

    def __init__(self):
        self.is_p1_turn = True
        self.board = self.create_board()
        self.init_state = [
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
        ]

    def create_board(self):
        """ Creates board. Initializes games positions. """
        board = [
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
            [0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
        ]

        return board

    def move(self, coord, dest_coord):
        """
        Moves player piece from coord to dest_coord if posible. Changes player turn if move is completed.
        """
        player = 1 if self.is_p1_turn else 2
        if self.is_valid_move(coord, dest_coord):
            self.board[coord[1]-1][coord[0]-1] = 0 # Remove player piece from initial coord.
            self.board[dest_coord[1]-1][dest_coord[0]-1] = player # Add player piece to destination.
            pp.pprint(self.board)
            self.is_p1_turn = not self.is_p1_turn # Change turn
        
        else:
            print("El movimiento no es válido!")

    def is_valid_move(self, coord, dest_coord):
        """ Checks if the move intended is valid. """
        player = 1 if self.is_p1_turn else 2
        if self.board[coord[1]-1][coord[0]-1] == player: # Check if initial coord is valid for player.
            valid_moves = self.valid_moves(coord) # Obtains valid moves from inital coord for player
            if dest_coord in valid_moves:
                return True
        
        return False

    def valid_moves(self, coord:tuple, hoop:bool=False, valid_coords:list=[]):
        """ Obtains frontier (searches valid moves) for a given coordinate. """

        self.check_direction(coord=coord, delta_x=1, delta_y=0, hoop=hoop, valid_coords=valid_coords) #horizontal +
        self.check_direction(coord=coord, delta_x=-1, delta_y=0, hoop=hoop, valid_coords=valid_coords) #horizontal -
        self.check_direction(coord=coord, delta_x=0, delta_y=1, hoop=hoop, valid_coords=valid_coords) #vertical +
        self.check_direction(coord=coord, delta_x=0, delta_y=-1, hoop=hoop, valid_coords=valid_coords) #vertical -
        self.check_direction(coord=coord, delta_x=1, delta_y=1, hoop=hoop, valid_coords=valid_coords) #major diagonal +
        self.check_direction(coord=coord, delta_x=-1, delta_y=-1, hoop=hoop, valid_coords=valid_coords) #major diagonal -
        self.check_direction(coord=coord, delta_x=1, delta_y=-1, hoop=hoop, valid_coords=valid_coords) #minor diagonal +
        self.check_direction(coord=coord, delta_x=-1, delta_y=1, hoop=hoop, valid_coords=valid_coords) #minor diagonal -

        return valid_coords

    def check_direction(self, coord:tuple, delta_x:int, delta_y:int, hoop:bool=False, valid_coords:list=[]):
        """
        Checks a direction (given by delta_x and delta_y) recursively appending valid moves to valid_coords list.
        """
        try:
            n_x = coord[0] + delta_x
            n_y = coord[1] + delta_y

            if not self.in_board(n_x, n_y): #Límites del tablero.
                return

            next_pos = self.board[n_y-1][n_x-1]

            if (next_pos==0) and (not hoop): #Primer movimiento válido.
                valid_coords.append((n_x, n_y))
                return

            elif (next_pos!=0): #Validar posible salto.
                if self.in_board(n_x+delta_x, n_y+delta_y) and (n_x+delta_x, n_y+delta_y) not in valid_coords:
                    if self.board[n_y+delta_y-1][n_x+delta_x-1]==0:
                        valid_coords.append((n_x+delta_x, n_y+delta_y))

                        return self.valid_moves(coord=(n_x+delta_x, n_y+delta_y),
                                                hoop=True,
                                                valid_coords=valid_coords)
                return

            else:
                return

        except Exception:
            return

    def in_board(self, X, Y):
        if X <= 10 and X >= 1 and Y <= 10 and Y >= 1:
            return True

        return False

    def is_winner(self):
        """ Checks of there is already a winner. """
        #Player 1
        is_p1_winner = True
        p1 = 5
        for j in range(0, 5):
            for i in range(p1, 0, -1):
                 is_p1_winner = is_p1_winner and self.board[j][i-1] == 2
            p1 -= 1

        #Player 2
        is_p2_winner = True
        p2 = 0
        for j in range(9, 4, -1):
            for i in range(9, p2+4, -1):
                is_p2_winner = is_p2_winner and self.board[i][j] == 1
            p2 += 1

        return is_p2_winner or is_p1_winner


