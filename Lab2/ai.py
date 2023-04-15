import copy

class AI:
    def __init__(self, algorithm, heuristic, max_tree_depth, player, enemy_player):
        if algorithm == 'minimax':
            self.predict_next_move = self.minimax
        elif algorithm == 'alphabeta':
            self.predict_next_move = self.alphabeta
        else:
            raise Exception("Incorrect algorithm chosen")
        
        if heuristic == 1:
            self.heuristic = self.heuristic1
        elif heuristic == 2:
            self.heuristic == self.heuristic2
        elif heuristic == 3:
            self.heuristic == self.heuristic3
        else:
            raise Exception("Incorrect heuristic chosen")
        
        self.max_tree_depth = max_tree_depth
        self.player = player
        self.enemy_player = enemy_player
        self.no_visited_nodes = 0

    def minimax(self, board, depth=0, maximizing_player=True):
        print('minimax')

    def alphabeta(self, board, depth=0, alpha=float('-inf'), beta=float('inf'), maximizing_player=True):
        print("alphabeta")

    # Maximalize the difference between the amount of our pons and enemy pons
    def heuristic1(self):
        print("heuristic1")

    # Maximalize the number of stable pons (pons that cannot be changed during the game)
    def heuristic2(self):
        print("heuristic2")

    def heuristic3(self):
        print("heuristic3")
