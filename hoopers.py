import pprint as pp
from tree import Node
import math
from copy import deepcopy


class Hoopers(object):
    """ Hoopers game class. Contains game state and methods. """

    def __init__(self, init_state):
        self.is_p1_turn = True
        self.board = self.get_state_board(init_state)
        self.curr_node = Node(state=init_state,
                              parent=None,
                              action=None,
                              value=None)

    def get_state_board(self, state):
        """ Creates board. Initializes games positions. """
        board = [
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
        ]

        for pair in state[0]: # Player 1
            board[pair[1]-1][pair[0]-1] = 1

        for pair in state[1]: # Player 2
            board[pair[1]-1][pair[0]-1] = 2
            
        return board

    def result(self, node:Node, action:tuple, player_one):
        """
        Defines the state resulting from taking an action in a given state.
        """
        player = 0 if player_one else 1
        new_state = deepcopy(node.state)
        new_state[player].remove(action[0])
        new_state[player].add(action[1])

        value = self.eval(new_state) # Evaluate node heuristic function value

        node = Node(state=new_state,
                    parent=node,
                    action=action,
                    value=value)

        return node

    def actions(self, node:Node, player_one:bool):
        """
        Gives set of legal moves in given node state.
        """
        actions = []
        player = 0 if player_one else 1
        for piece in node.state[player]:
            for dest in self.valid_moves(node, piece, hoop=False, valid_dests=[]):
                actions.append((piece, dest))
        return actions

    def move(self, coord:tuple, dest_coord:tuple):
        """
        Moves player piece from coord to dest_coord if posible. Changes player turn if move is completed.
        """
        if self.is_valid_move(coord, dest_coord):
            self.curr_node = self.result(self.curr_node, (coord, dest_coord), self.is_p1_turn)
            self.board = self.get_state_board(self.curr_node.state)
            self.is_p1_turn = not self.is_p1_turn # Change turn
            return True
        
        else:
            return False

    def is_valid_move(self, coord:tuple, dest_coord:tuple):
        """ Checks if the move intended is valid. """
        player = 0 if self.is_p1_turn else 1
        
        if coord in self.curr_node.state[player]: # Check if initial coord is valid for player.
            valid_moves = self.valid_moves(self.curr_node, coord, valid_dests=[]) # Obtains valid moves from inital coord for player
            if dest_coord in valid_moves:
                return True
        
        return False

    def valid_moves(self, node:Node, coord:tuple, hoop:bool=False, valid_dests:list=[]):
        """ Obtains frontier (searches valid moves) for a given coordinate. """

        self.check_direction(coord=coord, node=node, delta_x=1, delta_y=0, hoop=hoop, valid_dests=valid_dests) #horizontal +
        self.check_direction(coord=coord, node=node, delta_x=-1, delta_y=0, hoop=hoop, valid_dests=valid_dests) #horizontal -
        self.check_direction(coord=coord, node=node, delta_x=0, delta_y=1, hoop=hoop, valid_dests=valid_dests) #vertical +
        self.check_direction(coord=coord, node=node, delta_x=0, delta_y=-1, hoop=hoop, valid_dests=valid_dests) #vertical -
        self.check_direction(coord=coord, node=node, delta_x=1, delta_y=1, hoop=hoop, valid_dests=valid_dests) #major diagonal +
        self.check_direction(coord=coord, node=node, delta_x=-1, delta_y=-1, hoop=hoop, valid_dests=valid_dests) #major diagonal -
        self.check_direction(coord=coord, node=node, delta_x=1, delta_y=-1, hoop=hoop, valid_dests=valid_dests) #minor diagonal +
        self.check_direction(coord=coord, node=node, delta_x=-1, delta_y=1, hoop=hoop, valid_dests=valid_dests) #minor diagonal -

        return valid_dests

    def check_direction(self, coord:tuple, node:Node, delta_x:int, delta_y:int, hoop:bool=False, valid_dests:list=[]):
        """
        Checks a direction (given by delta_x and delta_y) recursively appending valid moves to valid_dests list.
        """
        board = self.get_state_board(node.state)

        try:
            n_x = coord[0] + delta_x
            n_y = coord[1] + delta_y

            if not self.in_board(n_x, n_y): #Límites del tablero.
                return

            next_pos = board[n_y-1][n_x-1]

            if (next_pos==0) and (not hoop): #Primer movimiento válido.
                valid_dests.append((n_x, n_y))
                return

            elif (next_pos!=0): #Validar posible salto.
                if self.in_board(n_x+delta_x, n_y+delta_y) and (n_x+delta_x, n_y+delta_y) not in valid_dests:
                    if board[n_y+delta_y-1][n_x+delta_x-1]==0:
                        valid_dests.append((n_x+delta_x, n_y+delta_y))

                        return self.valid_moves(node=node,
                                                coord=(n_x+delta_x, n_y+delta_y),
                                                hoop=True,
                                                valid_dests=valid_dests)
                return

            else:
                return

        except Exception:
            return

    def in_board(self, X:int, Y:int):
        if X <= 10 and X >= 1 and Y <= 10 and Y >= 1:
            return True

        return False

    def is_terminal(self, node:Node):
        """ A terminal test, which is true when the game is over and lfase otherwise. """
        board = self.get_state_board(node.state)

        #Player 1
        is_p1_winner = True
        p1 = 5
        for j in range(0, 5):
            for i in range(p1, 0, -1):
                 is_p1_winner = is_p1_winner and board[j][i-1] == 2
            p1 -= 1

        #Player 2
        is_p2_winner = True
        p2 = 0
        for j in range(9, 4, -1):
            for i in range(9, p2+4, -1):
                is_p2_winner = is_p2_winner and board[i][j] == 1
            p2 += 1

        return is_p2_winner or is_p1_winner

    def eval(self, state):
        """
        Estimates a state's utility.
        """
        heuristic = 0
        for piece in state[0]:
            heuristic += piece[0] + piece[1]
        for piece in state[1]:
            heuristic -= piece[0] + piece[1]
        return heuristic

    def minimax(self, node:Node, depth:int, alpha:float, beta:float, max_player:bool):
        """ Alpha Beta Search with player one as Max and player two as Min. """
        if depth==0 or self.is_terminal(node):
            return node.value, None

        if max_player:
            v = -math.inf
            move = None
            for action in self.actions(node, True): # Player 1 actions (MAX)
                v2, a2 = self.minimax(node = self.result(node, action, True),
                                      depth = depth-1,
                                      alpha = alpha,
                                      beta = beta,
                                      max_player = False)
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
                v2, a2 = self.minimax(node = self.result(node, action, False),
                                      depth = depth-1,
                                      alpha = alpha,
                                      beta = beta,
                                      max_player = True)
                if v2 < v:
                    v, move = v2, action
                    beta = min(beta, v)
                if beta <= alpha: # pruning
                    break
            return v, move

    def alpha_beta_search(self, node, depth):
        player = 1 if self.is_p1_turn else 0
        value, move = self.max_value(node, -math.inf, math.inf, depth)
        return move

    def max_value(self, node, alpha, beta, depth):
        if self.is_terminal(node) or depth<=0:
            return self.eval(node), None
        v = -math.inf
        for a in self.actions(node, True):
            v2, a2 = self.min_value(self.result(node, a, False), alpha, beta, depth-1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move

    def min_value(self, node, alpha, beta, depth):
        if self.is_terminal(node) or depth<=0:
            return self.eval(node), None
        v = math.inf
        for a in self.actions(node, True):
            v2, a2 = self.max_value(self.result(node, a, True), alpha, beta, depth-1)
            if v2 < v:
                v, move = v2, a
                alpha = min(alpha, v)
            if v >= beta:
                return v, move
