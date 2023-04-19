import copy

import numpy as np

class AI:
    def __init__(self, algorithm, heuristic, max_tree_depth, player, enemy_player):
        if algorithm == 'minimax' or algorithm == 'alphabeta':
            self.algorithm = algorithm
        else:
            raise Exception("Incorrect algorithm chosen")
        
        if heuristic == 1:
            self.heuristic = self.heuristic1
        elif heuristic == 2:
            self.heuristic = self.heuristic2
        elif heuristic == 3:
            self.heuristic = self.heuristic3
        else:
            raise Exception("Incorrect heuristic chosen")
        
        self.max_tree_depth = max_tree_depth
        self.player = player
        self.enemy_player = enemy_player
        self.no_visited_nodes = 0

    # In predicting next move we do the first iteration of minimax or alphabeta algorithm
    def predict_next_move(self, board):
        self.no_visited_nodes += 1
        best_move = None
        best_value = float('-inf')

        if self.algorithm == 'minimax':
            for move in board.get_all_possible_moves(self.player):
                new_board = copy.deepcopy(board)
                new_board.make_move(self.player, move)
                value = self.minimax(new_board, self.max_tree_depth-1, False)
                if value > best_value or best_move is None:
                    best_move = move
                    best_value = value

        # Algorithm can be simplified because beta will never change in this scenario
        elif self.algorithm == 'alphabeta':
            alpha = float('-inf')
            for move in board.get_all_possible_moves(self.player):
                new_board = copy.deepcopy(board)
                new_board.make_move(self.player, move)
                value = self.alphabeta(new_board, self.max_tree_depth-1, alpha, float('inf'), False)
                if value > best_value or best_move is None:
                    best_move = move
                    best_value = value
                alpha = max(alpha, value)

        return best_move

    def minimax(self, board, depth, maximizing_player):
        self.no_visited_nodes += 1

        if depth == 0 or not board.can_move_be_made:
            return self.heuristic(board)

        if maximizing_player:
            value = float('-inf')
            for move in board.get_all_possible_moves(self.player):
                new_board = copy.deepcopy(board)
                new_board.make_move(self.player, move)
                value = max(value, self.minimax(new_board, depth-1, False))
            return value
        else:
            value = float('inf')
            for move in board.get_all_possible_moves(self.enemy_player):
                new_board = copy.deepcopy(board)
                new_board.make_move(self.enemy_player, move)
                value = min(value, self.minimax(new_board, depth-1, True))
            return value

    def alphabeta(self, board, depth, alpha, beta, maximizing_player):
        self.no_visited_nodes += 1

        if depth == 0 or not board.can_move_be_made:
            return self.heuristic(board)

        if maximizing_player:
            value = float('-inf')
            for move in board.get_all_possible_moves(self.player):
                new_board = copy.deepcopy(board)
                new_board.make_move(self.player, move)
                value = max(value, self.alphabeta(new_board, depth-1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float('inf')
            for move in board.get_all_possible_moves(self.enemy_player):
                new_board = copy.deepcopy(board)
                new_board.make_move(self.enemy_player, move)
                value = min(value, self.alphabeta(new_board, depth-1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    # Maximalize the amount of our pons on the board
    def heuristic1(self, board):
        return board.get_no_pons(self.player)

    # Maximalize the number of stable pons (pons that cannot be overtaken during the game)
    def heuristic2(self, board):
        return board.get_no_stable_pons(self.player) - board.get_no_stable_pons(self.enemy_player)

    def heuristic3(self):
        print("heuristic3")
