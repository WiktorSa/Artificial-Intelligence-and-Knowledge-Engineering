from enum import Enum

class Players(Enum):
    FIRST_PLAYER = '1'
    SECOND_PLAYER = '2'

test_board = "0 0 0 0 0 0 0 0\n"
test_board += "0 0 0 0 0 0 0 0\n"
test_board += "0 0 0 0 0 0 0 0\n"
test_board += "0 0 0 1 2 0 0 0\n"
test_board += "0 0 0 2 1 0 0 0\n"
test_board += "0 0 0 0 0 0 0 0\n"
test_board += "0 0 0 0 0 0 0 0\n"
test_board += "0 0 0 0 0 0 0 0"

test_board2 = "0 2 2 2 2 2 2 1\n"
test_board2 += "1 1 1 1 1 1 1 1\n"
test_board2 += "1 1 1 1 1 1 1 1\n"
test_board2 += "1 1 1 1 1 1 1 1\n"
test_board2 += "1 1 1 1 1 1 1 1\n"
test_board2 += "1 1 1 1 1 1 1 1\n"
test_board2 += "1 1 1 1 1 1 1 1\n"
test_board2 += "1 1 1 1 1 1 1 1"

test_board3 = "0 0 0 0 0 0 0 0\n"
test_board3 += "0 1 2 0 0 0 0 0\n"
test_board3 += "0 2 1 2 1 2 2 0\n"
test_board3 += "0 2 0 1 2 0 2 0\n"
test_board3 += "0 2 0 2 1 0 2 0\n"
test_board3 += "0 1 1 1 1 1 2 0\n"
test_board3 += "0 1 1 2 2 1 2 0\n"
test_board3 += "0 0 0 0 0 0 0 0"
