
import os
import player
import numpy as np

class Neural(player.Player):
    def __init__(self, model, dumpScores=False):
        super().__init__()
        self.model = model
        self.dumpScores = dumpScores

    def select(self, game, board, color):
        cells = game.puttableCells(board, color)
        if len(cells) == 0:
            return None
        X_boards = np.array([game.put(board, color, p) for p in cells])
        X_colors = np.array([-color] * len(cells)).reshape([-1, 1])
        scores = self.model.predict([X_boards, X_colors], batch_size=len(cells))
        maximum = np.argmax(scores[:, color])

        if self.dumpScores:
            for cell, score in zip(cells, scores):
                print(cell, score)
            print("select:", cells[maximum])
        
        return cells[maximum]

class NeuralMTS(player.RandomMTS):
    def __init__(self, model, playoutNum=100, maxDepth=-1, dumpNodes=False):
        super().__init__(playoutNum, maxDepth, dumpNodes)
        self.model = model

    def playout(self, game, board, color):
        board = np.copy(board)
        while game.canPut(board):
            cells = game.puttableCells(board, color)
            if len(cells) > 0:
                X_boards = np.array([game.put(board, color, p) for p in cells])
                X_colors = np.array([-color] * len(cells)).reshape([-1, 1])
                scores = self.model.predict([X_boards, X_colors], batch_size=len(cells))[:, color]
                maximum = np.argmax(scores)
                board = game.put(board, color, cells[maximum])
            color = -color
        return game.judge(board)