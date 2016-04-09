#!/usr/bin/env python

import reversi
import random
import numpy

def playRandomly():
  game = reversi.Game()
  player = 1
  board = game.createBoard()
  
  history = [numpy.append(player, board.ravel())]
  
  while(True):
    #p = game.puttableRandom(board, player)
    #p = game.puttableMonteCarlo(board, player)
    p = game.puttableMonteCarloTreeSearch(board, player, 100)
    if(p is None):
      player = -player
      history.append(numpy.append(player, (board.ravel())))
      if(not game.canPut(board, player)):
        break
      continue
    
    print("player",player, "put",p)
    board = game.put(board, player, p)
    player = -player
    
    history.append(numpy.append(player, (board.ravel())))
    
    game.printBoard(board)
  
  win = game.judge(board)
  print("win:", win)
  return numpy.vstack(history).astype(float), numpy.vstack([[win]]*len(history)).astype(float)


def playRandomlyUnfair(stronger = 1):
  game = reversi.Game()
  player = 1
  board = game.createBoard()
  
  history = [numpy.append(player, board.ravel())]
  
  while(True):
    if(player == stronger):
      #p = game.puttableRandom(board, player)
      #p = game.puttableInput(board, player)
      p = game.puttableMonteCarloTreeSearch(board, player, 100)
    else:
      p = game.puttableRandom(board, player)
    
    if(p is None):
      player = -player
      history.append(numpy.append(player, (board.ravel())))
      if(not game.canPut(board, player)):
        break
      continue
    
    print("player",player, "put",p)
    board = game.put(board, player, p)
    player = -player
    
    history.append(numpy.append(player, (board.ravel())))
    
    game.printBoard(board)
  
  win = game.judge(board)
  print("win:", win)
  return numpy.vstack(history).astype(float), numpy.vstack([[win]]*len(history)).astype(float)
