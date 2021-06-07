""" Hoppers game implementation. """

from tree import Node
import math
import numpy as np


class Hoppers(object):
    """ Hoppers game class. Contains game state and methods. """

    def __init__(self, init_state:np.ndarray):
        self.player_one_turn = True
        
        self.board = self.get_state_board(init_state)
        self.moves_count = 1

        self.curr_node = Node(
            state=init_state,
            parent=None,
            action=None
        )


    def get_state_board(self, state:np.ndarray):
        """ Creates board. Initializes games positions. """

        board = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            dtype="uint32"
        )

        # Player 1
        for pair in state[0]:
            board[pair[1]][pair[0]] = 1

        # Player 2
        for pair in state[1]:
            board[pair[1]][pair[0]] = 2
            
        return board


    def result(self, node:Node, action:np.ndarray, player_one):
        """ Defines the state resulting from taking an action in a given state. """

        player = 0 if player_one else 1
        new_state = np.copy(node.state)
        
        new_state[player][(new_state[player] == action[0]).all(axis=1)] = action[1]

        node = Node(
            state=new_state,
            parent=node,
            action=action,
        )

        return node


    def actions(self, node:Node, player_one:bool):
        """ Gives set of legal moves in given node state. """

        actions = []

        player = 0 if player_one else 1

        for piece in node.state[player]:
            valid_moves = self.valid_moves(
                node=node,
                coord=piece,
                hoop=False,
                valid_dests=[]
            )

            for dest in valid_moves:
                actions.append((piece, dest))

        return actions


    def move(self, coord:np.ndarray, dest_coord:np.ndarray):
        """ Moves player piece from coord to dest_coord if posible. Changes player turn if move is completed. """

        # if self.is_valid_move(coord, dest_coord):
        self.curr_node = self.result(
            self.curr_node,
            (coord, dest_coord),
            self.player_one_turn
        )

        self.board = self.get_state_board(self.curr_node.state)
        self.player_one_turn = not self.player_one_turn # Change turn
        self.moves_count += 1
        print("Move number:", self.moves_count)

        return True
        
        return False


    def is_valid_move(self, coord:np.ndarray, dest_coord:np.ndarray):
        """ Checks if the move intended is valid. """

        player = 0 if self.player_one_turn else 1
        
        if coord in self.curr_node.state[player]: # Check if initial coord is valid for player.
            valid_moves = self.valid_moves(self.curr_node, coord, valid_dests=[]) # Obtains valid moves from inital coord for player
            if dest_coord in valid_moves:
                return True
        
        return False


    def valid_moves(
        self,
        node:Node,
        coord:np.ndarray,
        hoop:bool=False,
        valid_dests:list=[]
    ):
        """ Obtains frontier (searches valid moves) for a given coordinate. """

        deltas = [-1, 0, 1]

        for d_x in deltas:
            for d_y in deltas:
                if not (d_y==0 and d_x==0):
                    self.check_direction(
                        coord=coord,
                        node=node,
                        delta_x=d_x,
                        delta_y=d_y,
                        hoop=hoop,
                        valid_dests=valid_dests
                    )

        return valid_dests


    def check_direction(
        self,
        coord:np.ndarray,
        node:Node,
        delta_x:int,
        delta_y:int,
        hoop:bool=False,
        valid_dests:list=[]
    ):
        """ Checks a direction (given by delta_x and delta_y) recursively appending valid moves to valid_dests list. """

        board = self.get_state_board(node.state)
        n_x = coord[0] + delta_x
        n_y = coord[1] + delta_y

        if not self.in_board(n_x, n_y): #Límites del tablero.
            return

        next_pos = board[n_y][n_x]

        if (next_pos==0) and (not hoop): #Primer movimiento válido.
            valid_dests.append((n_x, n_y))
            return

        elif (next_pos!=0): #Validar posible salto.
            hoop_x, hoop_y = n_x+delta_x, n_y+delta_y
            if self.in_board(hoop_x, hoop_y) and (hoop_x, hoop_y) not in valid_dests:
                if board[hoop_y][hoop_x]==0:
                    valid_dests.append((hoop_x, hoop_y))

                    return self.valid_moves(
                        node=node,
                        coord=(hoop_x, hoop_y),
                        hoop=True,
                        valid_dests=valid_dests
                    )
            return

        else:
            return


    def in_board(self, X:int, Y:int):
        if X <= 9 and X >= 0 and Y <= 9 and Y >= 0:
            return True

        return False


    def is_terminal(self, node:Node):
        """ A terminal test, which is true when the game is over and lfase otherwise. """

        #Player 1
        p1_wins = np.array([
            (5,9), (6,9), (7,9), (8,9), (9,9),
            (6,8), (7,8), (8,8), (9,8), (7,7),
            (8,7), (9,7), (8,6), (9,6), (9,5)
        ])

        #Player 2
        p2_wins = np.array([
            (0,0), (0,1), (0,2), (0,3), (0,4),
            (1,0), (1,1), (1,2), (1,3), (2,0),
            (2,1), (2,2), (3,0), (3,1), (4,0)
        ])

        return np.isin(node.state[0], p1_wins).all() or np.isin(node.state[1], p2_wins).all()


    def eval(self, state):
        """ Estimates a state's utility.

            Euclidean distance to objective.
            Distance from origin minus distance from objective.
        """

        return ( ( state[0]**2 - (state[0]-9)**2 ) - ( (state[1]-9)**2 - state[1]**2 ) ).sum()
        # return ( - (state[0]-9)**2 + state[1]**2 ).sum()


    def alpha_beta_search(self, node:Node, depth:int, max_player:bool):
        player = 1 if self.player_one_turn else 0

        if max_player:
            value, move = self.max_value(node, -math.inf, math.inf, depth)
        else:
            value, move = self.min_value(node, -math.inf, math.inf, depth)

        return value, move


    def max_value(self, node:Node, alpha:float, beta:float, depth:int):
        if self.is_terminal(node) or depth<=0:
            return self.eval(node.state), None

        v = -math.inf
        for a in self.actions(node, player_one=True):
            v2, a2 = self.min_value(
                self.result(node, a, player_one=True),
                alpha,
                beta,
                depth-1
            )
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move

        return v, move


    def min_value(self, node:Node, alpha:float, beta:float, depth:int):
        if self.is_terminal(node) or depth<=0:
            return self.eval(node.state), None

        v = math.inf
        for a in self.actions(node, player_one=False):
            v2, a2 = self.max_value(
                self.result(node, a, player_one=False),
                alpha,
                beta,
                depth-1
            )
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move

        return v, move


    def minimax(
        self,
        node:Node,
        depth:int,
        alpha:float,
        beta:float,
        max_player:bool
    ):
        """ Alpha Beta Search with player one as Max and player two as Min. """

        if depth==0 or self.is_terminal(node):
            return node.value, None

        if max_player:
            v = -math.inf
            move = None

            for action in self.actions(node, True): # Player 1 actions (MAX)
                v2, a2 = self.minimax(
                    node = self.result(node, action, True),
                    depth = depth-1,
                    alpha = alpha,
                    beta = beta,
                    max_player = False
                )

                if v2 > v:
                    v, move = v2, action
                    alpha = max(alpha, v)

                if beta <= alpha: #pruning
                    break

            return v, move

        else:
            v = math.inf
            move = None

            for action in self.actions(node, False): # Player 2 actions (MIN)
                v2, a2 = self.minimax(
                    node = self.result(node, action, False),
                    depth = depth-1,
                    alpha = alpha,
                    beta = beta,
                    max_player = True
                )

                if v2 < v:
                    v, move = v2, action
                    beta = min(beta, v)

                if beta <= alpha: # pruning
                    break

            return v, move
