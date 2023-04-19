import numpy as np
from players import Players

class Board:
    BOARD_SIZE = 8

    def __init__(self, board_str):
        self.board = self._set_game(board_str)

    # From the input string set the gaming board
    def _set_game(self, board_str):
        board = []
        for row in board_str.split('\n'):
            board.append(row.split(' '))
        return np.array(board)

    def make_move(self, player, cell_location):
        if self._is_move_possible(player, cell_location):
            self.board[cell_location] = player.value
            for x_direction, y_direction in self._get_all_directions(player, cell_location):
                # We limit the number of checks because there are reduntant
                for i in range(1, self.BOARD_SIZE):
                    x_location = cell_location[0] + i * x_direction
                    y_location = cell_location[1] + i * y_direction
                    nxt_cell = self.board[x_location, y_location]
                    if nxt_cell != player.value:
                        self.board[x_location, y_location] = player.value
                    else:
                        break
        else:
            raise Exception("Illegal move made by the program. Check for possible errors within the code")

    def get_all_possible_moves(self, player):
        all_possible_moves = []
        for index, _ in np.ndenumerate(self.board):
            if self._is_move_possible(player, index):
                all_possible_moves.append(index)
        
        # Sometimes player cannot make a move - an array with None value will express it
        if not all_possible_moves:
            all_possible_moves.append(None)

        return all_possible_moves
    
    def _is_move_possible(self, player, cell_location):
        # You cannot place a piece on top of another player
        if self.board[cell_location] == Players.FREE_SPACE.value:
            if player == Players.FIRST_PLAYER:
                other_player = Players.SECOND_PLAYER
            else:
                other_player = Players.FIRST_PLAYER

            # Check every direction. If any of them allows for this move than return True
            for x_direction, y_direction in [(x, y) for x in range(-1, 2) for y in range(-1, 2)]:
                is_other_player_between = False
                for i in range(1, 8):
                    x_location = cell_location[0] + i * x_direction
                    y_location = cell_location[1] + i * y_direction
                    if x_location < 0 or x_location > self.BOARD_SIZE-1 or y_location < 0 or y_location > self.BOARD_SIZE-1:
                        break

                    nxt_cell = self.board[x_location, y_location]
                    if nxt_cell == other_player.value:
                        is_other_player_between = True
                    elif nxt_cell == player.value and is_other_player_between:
                        return True
                    else:
                        break
        
        return False

    def _get_all_directions(self, player, cell_location):
        if player == Players.FIRST_PLAYER:
                other_player = Players.SECOND_PLAYER
        else:
            other_player = Players.FIRST_PLAYER

        # Check every direction. If a direction meets the condition than save it
        directions = []
        for x_direction, y_direction in [(x, y) for x in range(-1, 2) for y in range(-1, 2)]:
            is_other_player_between = False
            for i in range(1, self.BOARD_SIZE):
                x_location = cell_location[0] + i * x_direction
                y_location = cell_location[1] + i * y_direction

                if x_location < 0 or x_location > self.BOARD_SIZE-1 or y_location < 0 or y_location > self.BOARD_SIZE-1:
                    break

                nxt_cell = self.board[x_location, y_location]
                if nxt_cell == other_player.value:
                    is_other_player_between = True
                elif nxt_cell == player.value and is_other_player_between:
                    directions.append((x_direction, y_direction))
                    break
                else:
                    break

        return directions

    @property
    def can_move_be_made(self):
        first_player_moves = self.get_all_possible_moves(Players.FIRST_PLAYER)
        second_player_moves = self.get_all_possible_moves(Players.SECOND_PLAYER)
        return first_player_moves != [None] or second_player_moves != [None]

    def __str__(self):
        board_str = ""
        for row in self.board:
            for cell in row:
                board_str += cell
                board_str += " "
            board_str += "\n"
            
        return board_str
    
    def get_no_pons(self, player):
        return np.count_nonzero(self.board == player.value)
    
    # Stable pon is the pon that cannot change colour during the game
    def get_no_stable_pons(self, player):
        no_stable_pons = 0
        for index, _ in np.ndenumerate(self.board):
            if self.board[index] == player.value and self._is_stable_pon(player, index):
                no_stable_pons += 1

        return no_stable_pons

    # There are 2 conditions that need to be met for the pon to be considered unstable
    # 1. There are 2 free spaces on which if enemy places its pons it will overtake our pon
    # 2. There is 1 free space on which if enemy places its pon it will overtake our pon
    # Note - The conditions for stable pons are much more complex but we assume that we won't perform movements that will make the pon unstable
    def _is_stable_pon(self, player, cell_location):
        if player == Players.FIRST_PLAYER:
            other_player = Players.SECOND_PLAYER
        else:
            other_player = Players.FIRST_PLAYER

        for x_direction, y_direction in [(1, 0), (1, 1), (0, 1), (-1, 1)]:
            found_free_space = False
            found_enemy_pon = False
            for i in range(1, self.BOARD_SIZE):
                x_location = cell_location[0] + i * x_direction
                y_location = cell_location[1] + i * y_direction
                if x_location < 0 or x_location > self.BOARD_SIZE-1 or y_location < 0 or y_location > self.BOARD_SIZE-1:
                    break

                if self.board[x_location][y_location] == Players.FREE_SPACE.value:
                    found_free_space = True
                    break
                elif self.board[x_location][y_location] == other_player.value:
                    found_enemy_pon = True
                    break
            
            # Only if we have the possiblity to overtake the pon we will analyse the opposite direction
            if found_free_space or found_enemy_pon:
                for i in range(1, self.BOARD_SIZE):
                    x_location = cell_location[0] + i * x_direction * (-1)
                    y_location = cell_location[1] + i * y_direction * (-1)
                    if x_location < 0 or x_location > 7 or y_location < 0 or y_location > 7:
                        break

                    if self.board[x_location][y_location] == Players.FREE_SPACE.value:
                        return False
                    elif self.board[x_location][y_location] == other_player.value and found_free_space:
                        return False

        return True
