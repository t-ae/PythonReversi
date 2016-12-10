#!/usr/bin/env python

import os, time
import numpy as np
import reversi
import player


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "record")
DUMP_BOARD = True

game = reversi.Game()

# player.RandomUniform()
# player.RandomMTS(100, 5)
playerA = player.RandomUniform()
playerB = player.RandomMTS(50, 1, True)

# kougo
blackPlayer = playerA
whitePlayer = playerB
for i in range(1, 9999999):
    print("game:", i, end='\n' if DUMP_BOARD else "\r")

    board = game.createBoard()
    if DUMP_BOARD:
        game.printBoard(board)

    X_boards = []
    X_colors = []
    while True:

        cellA = blackPlayer.select(game, board, reversi.BLACK)
        if cellA is not None:
            board = game.put(board, reversi.BLACK, cellA)
        
        # append
        X_boards.append(board)
        X_colors.append(reversi.WHITE)
        X_boards.append(np.transpose(board))
        X_colors.append(reversi.WHITE)
        X_boards.append(np.rot90(board, 2))
        X_colors.append(reversi.WHITE)
        X_boards.append(np.rot90(np.transpose(board), 2))
        X_colors.append(reversi.WHITE)

        if DUMP_BOARD and cellA is not None:
            game.printBoard(board)

        cellB = whitePlayer.select(game, board, reversi.WHITE)
        if cellB is not None:
            board = game.put(board, reversi.WHITE, cellB)
        
        # append
        X_boards.append(board)
        X_colors.append(reversi.BLACK)
        X_boards.append(np.transpose(board))
        X_colors.append(reversi.BLACK)
        X_boards.append(np.rot90(board, 2))
        X_colors.append(reversi.BLACK)
        X_boards.append(np.rot90(np.transpose(board), 2))
        X_colors.append(reversi.BLACK)

        if DUMP_BOARD and cellB is not None:
            game.printBoard(board)

        if cellA is None and cellB is None:
            break
    
    won = game.judge(board)
    if DUMP_BOARD:
        print("won:", won)

    # create y
    y = np.zeros([3])
    y[won] = 1

    now = int(round(time.time()*1000))
    path = os.path.join(OUTPUT_DIR, "{0}.npz".format(now))

    np.savez(path, 
             X_board=np.array(X_boards).reshape([-1, 8, 8]),
             X_color=np.array(X_colors).reshape([-1, 1]), 
             y=y)
    
    # change
    tmp = blackPlayer
    blackPlayer = whitePlayer
    whitePlayer = tmp