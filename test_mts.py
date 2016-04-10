#!/usr/bin/env python

import random_play
import reversi
import numpy

board = numpy.zeros([8,8])
board[1,2] = 1
board[0,3] = 1
board[1,3] = 1
board[2,3] = -1
board[3,3] = 1

reversi.game.printBoard(board)

p = reversi.game.puttableMonteCarloTreeSearch(board, -1, 100)
print(p)