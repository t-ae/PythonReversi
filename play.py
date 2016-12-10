#!/usr/bin/env python

import reversi
import player
import numpy as np

game = reversi.Game()

playerA = player.StdInput(reversi.BLACK)
playerB = player.RandomMTS(reversi.WHITE)

board = game.createBoard()

while(True):
    cellA = playerA.select(game, board)
    if(cellA is not None):
        board = game.put(board, playerA.color, cellA)
    
    if(cellA is not None):
        game.printBoard(board)
    cellB = playerB.select(game, board)
    if(cellB is not None):
        board = game.put(board, playerB.color, cellB)
    
    if(cellB is not None):
        game.printBoard(board)
    
    if(cellA is None and cellB is None):
        break

won = game.judge(board)
if(won==reversi.BLACK):
    print("you won")
elif(won==reversi.WHITE):
    print("you lose")
else:
    print("draw")