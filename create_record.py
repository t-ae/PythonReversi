#!/usr/bin/env python

import reversi
import player
import numpy as np

DUMP_BOARD = True

game = reversi.Game()

playerA = player.RandomUniform(reversi.BLACK)
playerB = player.RandomMTS(reversi.WHITE)

while(True):
    board = game.createBoard()

    while(True):

        cellA = playerA.select(game, board)
        if(cellA is not None):
            board = game.put(board, playerA.color, cellA)
        
        if(DUMP_BOARD and cellA is not None):
            game.printBoard(board)

        cellB = playerB.select(game, board)
        if(cellB is not None):
            board = game.put(board, playerB.color, cellB)
        
        if(DUMP_BOARD and cellB is not None):
            game.printBoard(board)
        
        if(cellA is None and cellB is None):
            break
    
    print("won:", game.judge(board))
    break