import time

from config import test_board, test_board2, test_board3
from players import Players
from board import Board
from ai import AI

def main(board_str):
    POSSIBLE_ALGORITHMS = ['minimax', 'alphabeta']
    POSSIBLE_HEURISTIC = [1, 2, 3]
    POSSIBLE_MAX_TREE_DEPTH = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    board = Board(board_str)
    first_player = AI(POSSIBLE_ALGORITHMS[1], POSSIBLE_HEURISTIC[0], POSSIBLE_MAX_TREE_DEPTH[3], Players.FIRST_PLAYER, Players.SECOND_PLAYER)
    second_player = AI(POSSIBLE_ALGORITHMS[1], POSSIBLE_HEURISTIC[1], POSSIBLE_MAX_TREE_DEPTH[3], Players.SECOND_PLAYER, Players.FIRST_PLAYER)

    # Playing game
    start_time = time.time()
    no_turn = 0
    cur_player = first_player
    while board.can_move_be_made:
        if cur_player == first_player:
            no_turn += 1

        move = cur_player.predict_next_move(board)
        # Sometimes player cannot make a move
        if move:
            board.make_move(cur_player.player, move)

        if cur_player == first_player:
            cur_player = second_player
        else:
            cur_player = first_player
    end_time = time.time()

    # Decide who won
    dif_pons = board.get_no_pons(Players.FIRST_PLAYER) - board.get_no_pons(Players.SECOND_PLAYER)
    if dif_pons > 0:
        win_player = 'Player1'
    elif dif_pons == 0:
        win_player = 'Tie'
    else:
        win_player = 'Player2'

    # Printing results
    print(board)
    print(f'No turns: {no_turn}, Winning Player: {win_player}')
    print(f'Number of visited nodes for Player1: {first_player.no_visited_nodes}')
    print(f'Number of visited nodes for Player2: {second_player.no_visited_nodes}')
    print(f'Length of the game: {end_time - start_time:.2f} seconds')

if __name__ == '__main__':
    main(test_board)