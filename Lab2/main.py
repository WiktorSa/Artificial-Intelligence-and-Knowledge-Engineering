from config import test_board, test_board2, test_board3, Players
from board import Board
from ai import AI

def main(board_str):
    POSSIBLE_ALGORITHMS = ['minimax', 'alphabeta']
    POSSIBLE_HEURISTIC = [1, 2, 3]
    POSSIBLE_MAX_TREE_DEPTH = [1, 3, 5, 7, 10]

    board = Board(board_str)
    ai_player1 = AI(POSSIBLE_ALGORITHMS[0], POSSIBLE_HEURISTIC[0], POSSIBLE_MAX_TREE_DEPTH[0], Players.FIRST_PLAYER, Players.SECOND_PLAYER)
    ai_player2 = AI(POSSIBLE_ALGORITHMS[0], POSSIBLE_HEURISTIC[0], POSSIBLE_MAX_TREE_DEPTH[0], Players.SECOND_PLAYER, Players.FIRST_PLAYER)
    ai_player1.predict_next_move(None)
    


if __name__ == '__main__':
    main(test_board)