#!/usr/bin/env python

import os
import numpy as np
import reversi, neural_player
from keras.models import load_model

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.h5")
model = load_model(MODEL_PATH)

player = neural_player.Neural(model)

game = reversi.Game()

for i in range(1, 999999):
    board = game.createBoard()
    X_boards = []
    X_colors = []

    while True:
        cellA = player.select(game, board, reversi.BLACK)
        if cellA is not None:
            board = game.put(board, reversi.BLACK, cellA)
        X_boards.append(board)
        X_colors.append(reversi.WHITE)
        X_boards.append(np.transpose(board))
        X_colors.append(reversi.WHITE)

        cellB = player.select(game, board, reversi.WHITE)
        if cellB is not None:
            board = game.put(board, reversi.WHITE, cellB)
        X_boards.append(board)
        X_colors.append(reversi.BLACK)
        X_boards.append(np.transpose(board))
        X_colors.append(reversi.BLACK)

        if cellA is None and cellB is None:
            break
    
    won = game.judge(board)

    X_board = np.array(X_boards).reshape([-1, 8, 8])
    X_color = np.array(X_colors).reshape([-1, 1])
    y = np.zeros([3])
    y[won] = 1
    y = np.concatenate([y.reshape([1, 3])]*len(X_color), axis=0)

    loss, acc = model.train_on_batch([X_board, X_color], y)
    print("{0:5d}: won: {1}, loss: {2:3.5f}, acc: {3:3.5f}".format(i, won, loss, acc),end='\r')
    
    if i%100==0:
        print("\nsave model")
        model.save(MODEL_PATH)