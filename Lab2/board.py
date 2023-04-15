import numpy as np
from config import Players

class Board:
    def __init__(self, board_str):
        self.board = self._set_game(board_str)

    # From the input string set the gaming board
    def _set_game(self, board_str):
        board = []
        for row in board_str.split('\n'):
            board.append(row.split(' '))
        return np.array(board)

    def make_move(self, cur_player, cell_location):
        if self._is_move_possible(cur_player, cell_location):
            self.board[cell_location] = cur_player.value
            for x_direction, y_direction in self._get_all_directions(cur_player, cell_location):
                # We limit the number of checks because there are reduntant
                for i in range(1, 8):
                    x_location = cell_location[0] + i * x_direction
                    y_location = cell_location[1] + i * y_direction
                    nxt_cell = self.board[x_location, y_location]
                    if nxt_cell != cur_player.value:
                        self.board[x_location, y_location] = cur_player.value
                    else:
                        break
        else:
            raise Exception("Illegal move made by the program. Check for possible errors within the code")

    def get_all_possible_moves(self, cur_player):
        all_possible_moves = []
        for index, _ in np.ndenumerate(self.board):
            if self._is_move_possible(cur_player, index):
                all_possible_moves.append(index)

        return all_possible_moves
    
    def _is_move_possible(self, cur_player, cell_location):
        # You cannot place a piece on top of another player
        if self.board[cell_location] == '0':
            if cur_player == Players.FIRST_PLAYER:
                other_player = Players.SECOND_PLAYER
            else:
                other_player = Players.FIRST_PLAYER

            # Check every direction. If any of them allows for this move than return True
            for x_direction, y_direction in [(x, y) for x in range(-1, 2) for y in range(-1, 2)]:
                is_other_player_between = False
                for i in range(1, 8):
                    x_location = cell_location[0] + i * x_direction
                    y_location = cell_location[1] + i * y_direction
                    if x_location < 0 or x_location > 7 or y_location < 0 or y_location > 7:
                        break

                    nxt_cell = self.board[x_location, y_location]
                    if nxt_cell == other_player.value:
                        is_other_player_between = True
                    elif nxt_cell == cur_player.value and is_other_player_between:
                        return True
                    else:
                        break
        
        return False

    def _get_all_directions(self, cur_player, cell_location):
        if cur_player == Players.FIRST_PLAYER:
                other_player = Players.SECOND_PLAYER
        else:
            other_player = Players.FIRST_PLAYER

        # Check every direction. If a direction meets the condition than save it
        directions = []
        for x_direction, y_direction in [(x, y) for x in range(-1, 2) for y in range(-1, 2)]:
            is_other_player_between = False
            for i in range(1, 8):
                x_location = cell_location[0] + i * x_direction
                y_location = cell_location[1] + i * y_direction

                if x_location < 0 or x_location > 7 or y_location < 0 or y_location > 7:
                    break

                nxt_cell = self.board[x_location, y_location]
                if nxt_cell == other_player.value:
                    is_other_player_between = True
                elif nxt_cell == cur_player.value and is_other_player_between:
                    directions.append((x_direction, y_direction))
                    break
                else:
                    break

        return directions

    @property
    def can_move_be_made(self):
        first_player_moves = self.get_all_possible_moves(Players.FIRST_PLAYER)
        second_player_moves = self.get_all_possible_moves(Players.SECOND_PLAYER)
        return first_player_moves != [] or second_player_moves != []

    def __str__(self):
        board_str = ""
        for row in self.board:
            for cell in row:
                board_str += cell
                board_str += " "
            board_str += "\n"
            
        return board_str
