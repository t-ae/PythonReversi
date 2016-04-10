#!/usr/bin/env python

import random_play
import reversi
import numpy

board = numpy.zeros([8,8])
board[3,3] = 1
board[3,4] = 1
board[4,4] = -1
board[5,4] = -1

reversi.game.printBoard(board)

p = reversi.game.puttableMonteCarloTreeSearch(board, 1, )
print(p)