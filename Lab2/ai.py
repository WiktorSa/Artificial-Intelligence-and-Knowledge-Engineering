import copy

from players import Players

import numpy as np

class AI:
    SORT_VALUES_ALPHABETA = True

    def __init__(self, algorithm, heuristic, max_tree_depth, player, enemy_player):
        if algorithm == 'minimax' or algorithm == 'alphabeta' or algorithm == 'human':
            self.algorithm = algorithm
        else:
            raise Exception("Incorrect algorithm chosen")
        
        if heuristic == 1:
            self.heuristic = self.heuristic1
        elif heuristic == 2:
            self.heuristic = self.heuristic2
        elif heuristic == 3:
            self.heuristic = self.heuristic3
        elif heuristic == 4:
            self.heuristic = self.heuristic4
        elif heuristic == 5:
            self.heuristic = self.heuristic5_adaptive
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
                if value > best_value:
                    best_move = move
                    best_value = value

        # Algorithm can be simplified because beta will never change in this iteration
        elif self.algorithm == 'alphabeta':
            # Sort moves based on the first heuristic to possibly decrease the number of visited nodes
            if self.SORT_VALUES_ALPHABETA:
                all_moves = {}
                for move in board.get_all_possible_moves(self.player):
                    new_board = copy.deepcopy(board)
                    new_board.make_move(self.player, move)
                    all_moves[move] = self.heuristic(new_board)

                all_moves = dict(sorted(all_moves.items(), key=lambda item: item[1], reverse=True))

            else:
                all_moves = {k: 0 for k in board.get_all_possible_moves(self.player)}

            alpha = float('-inf')
            for move in all_moves.keys():
                new_board = copy.deepcopy(board)
                new_board.make_move(self.player, move)
                value = self.alphabeta(new_board, self.max_tree_depth-1, alpha, float('inf'), False)
                if value > best_value:
                    best_move = move
                    best_value = value
                alpha = max(alpha, value)

        elif self.algorithm == 'human':
            best_move = self.make_move_player(board)

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
        
    def make_move_player(self, board):
        all_possible_moves = board.get_all_possible_moves(self.player)
        all_possible_moves_player = [(x[0]+1, x[1]+1) for x in all_possible_moves]
        print("Choose one of the moves below")
        for move in all_possible_moves_player:
            print(f'Row: {move[0]}, Column: {move[1]}')
        
        while True:
            inp = input("Choose row and column. Separate values by space\n")
            inp = inp.split()
            try:
                if len(inp) == 2:
                    inp = (int(inp[0]), int(inp[1]))
                    if inp in all_possible_moves_player:
                        print()
                        return (inp[0]-1, inp[1]-1)
            except ValueError:
                pass

            print("Incorrect input")

    # Maximalize the amount of our pons on the board
    def heuristic1(self, board):
        return board.get_no_pons(self.player)

    # Maximalize the number of stable pons (pons that cannot be overtaken during the game)
    # The enemy will try to maximalize their number of stable pons
    def heuristic2(self, board):
        return board.get_no_stable_pons(self.player) - board.get_no_stable_pons(self.enemy_player)

    # Minimalize the number of moves that the opponent can take
    def heuristic3(self, board):
        all_enemy_moves = board.get_all_possible_moves(self.enemy_player)
        all_enemy_moves = list(filter(None, all_enemy_moves))
        return (-1) * len(all_enemy_moves)

    # Maximalize the amount of our pons on the board but priotize fields on the corners of the board
    def heuristic4(self, board):
        return board.get_no_pons_priority(self.player)
    
    # Complex heuristic
    # It uses the following ruling
    # 1. Until there are no stable pons than just increase your board coverage
    # 2. Try to insure that you are the last person to make a move on the board
    # That means that if you are the first player you want to have the even amount of pons on the board
    # 3. If opponent has a lot of move available and thus it's likely not possible to quickly reduce its number of moves to 0 than just increase the number of stable pons
    def heuristic5_adaptive(self, board):
        no_pons_board = board.get_no_pons(self.player) + board.get_no_pons(self.enemy_player)

        # Increase advantage at the beginning of the game
        if board.get_no_stable_pons(self.player) == 0 and board.get_no_stable_pons(self.enemy_player) == 0:
            return self.heuristic4(board)
        
        # Enemy has too many moves that it will be impossible to quickly reduce it to 0
        all_enemy_moves = board.get_all_possible_moves(self.enemy_player)
        all_enemy_moves = list(filter(None, all_enemy_moves))
        if len(all_enemy_moves) >= 3:
            return self.heuristic2(board)
        
        # Determine if you can insure that you will make the final move
        if self.player == Players.FIRST_PLAYER and no_pons_board % 2 == 1:
            return self.heuristic2(board)
        elif self.player == Players.SECOND_PLAYER and no_pons_board % 2 == 0:
            return self.heuristic2(board)
        else:
            return self.heuristic3(board)
