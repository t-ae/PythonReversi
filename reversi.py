#!/usr/bin/env python

import numpy
import random

# board 8x8 int array
# BLACK=1 white=-1

EMPTY = 0
BLACK = 1
WHITE = -1

class Game:
    def __init__(self):
        __range = [0, 1, 2, 3, 4, 5, 6, 7]
        self.__positions = [(x, y) for x in __range for y in __range]
        self.__ds = [(dx, dy) for dx in [0, -1, 1] for dy in [0, -1, 1]][1:]

    def createBoard(self):
        board = numpy.zeros([8, 8], dtype=int)
        board[3, 3] = WHITE
        board[4, 4] = WHITE
        board[3, 4] = BLACK
        board[4, 3] = BLACK
        return board

    def printBoard(self, board):
        for y in range(-1, 8):
            for x in range(-1, 8):
                if x == -1 and y == -1:
                    print(" ", end="")
                elif x == -1:
                    print("ABCDEFGH"[y], end="")
                elif y == -1:
                    print(" "+"12345678"[x], end="")
                elif board[x, y] == 1:
                    print(" X", end="")
                elif board[x, y] == -1:
                    print(" O", end="")
                else:
                    print(" .", end="")
            print("")

    # bools
    def isInBoard(self, position):
        return 0 <= position[0] and position[0] < 8 and 0 <= position[1] and position[1] < 8

    def canPut(self, board, color = None, position = None):
        if color is None:
            return self.canPut(board, BLACK) or self.canPut(board, WHITE)
        elif position is None:
            for pos in self.__positions:
                if self.canPut(board, color, pos):
                    return True
            return False
        elif not self.isInBoard(position) or board[position] != EMPTY:
            return False
        else:
            for ds in self.__ds:
                if self.__canPutSub(board, color, position, ds):
                    return True
            return False

    def __canPutSub(self, board, color, position, ds, r = False):
        nowPos = (position[0] + ds[0], position[1] + ds[1])
        if not self.isInBoard(nowPos):
            return False
        if board[nowPos] == EMPTY:
            return False
        elif board[nowPos] == color:
            return r
        else:
            return self.__canPutSub(board, color, nowPos, ds, True)
    
    # return board(numpy.ndarray)
    def put(self, board, color, position):
        board = numpy.copy(board)
        if board[position] != EMPTY:
            raise Exception("Try to put invalid place.")
        board[position] = color
        for ds in self.__ds:
            self.__putSub(board, color, position, ds)
        return board

    def __putSub(self, board, color, position, ds):
        nowPos = (position[0] + ds[0], position[1] + ds[1])
        if not self.isInBoard(nowPos):
            return False
        elif board[nowPos] == EMPTY:
            return False
        elif board[nowPos] == color:
            return True
        elif self.__putSub(board, color, nowPos, ds):
            board[nowPos] = color
            return True
        else:
            return False

    def judge(self, board):
        s = numpy.sum(board)
        if s > 0:
            return BLACK
        elif s < 0:
            return WHITE
        else:
            return EMPTY

    def puttableCells(self, board, color):
        puttables = []
        for pos in self.__positions:
            if self.canPut(board, color, pos):
                puttables.append(pos)
        return puttables
