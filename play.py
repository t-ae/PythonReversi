#!/usr/bin/env python

import os, random
import reversi, player, neural_player
from keras.models import load_model

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.h5")
model = load_model(MODEL_PATH)
# player.RandomUniform()
# player.RandomMTS(100, 5)
# neural_player.Neural(model)
# neural_player.NeuralMTS(model, 30, 2)
opponent = neural_player.Neural(model, True)


game = reversi.Game()
board = game.createBoard()
game.printBoard(board)



if bool(random.getrandbits(1)):
    playerColor = reversi.BLACK
    blackPlayer = player.StdInput()
    whitePlayer = opponent
else:
    playerColor = reversi.WHITE
    whitePlayer = player.StdInput()
    blackPlayer = opponent

while True:
    cellA = blackPlayer.select(game, board, reversi.BLACK)
    if cellA is not None:
        board = game.put(board, reversi.BLACK, cellA)
    
    if cellA is not None:
        game.printBoard(board)
    cellB = whitePlayer.select(game, board, reversi.WHITE)
    if cellB is not None:
        board = game.put(board, reversi.WHITE, cellB)
    
    if cellB is not None:
        game.printBoard(board)
    
    if cellA is None and cellB is None:
        break

won = game.judge(board)
if won == playerColor:
    print("you won")
elif won == -playerColor:
    print("you lose")
else:
    print("draw")