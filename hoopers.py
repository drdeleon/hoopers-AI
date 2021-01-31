import pprint as pp


class Hoopers(object):
    """ Hoopers game class. Contains game state and methods. """

    def __init__(self):
        self.is_p1_turn = True
        self.board = self.create_board()

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

        pp.pprint(board)
        return board

    def move(self, player, piece_coord, dest_coord):
        pass

    def is_valid_move(self, player, piece_coord, dest_coord):
        """ Checks if the move intended is valid. """
        pass

    def valid_moves(self, player, pieceCoord):
        """ docstring """
        pass

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


