#!/usr/bin/env python

import reversi
import random
import numpy

import nn

def puttableNN(board, player):
  puttables = reversi.game.puttables(board, player)
  #print("candidate:", puttables)
  max = -10000
  ret = None
  for p in puttables:
    b = reversi.game.put(board, player, p)
    data = numpy.append(player, b.ravel()).astype(float).reshape([1,65])
    score = player*nn.neuralNet.evaluate(data)
    #print("p:",p,"score:",score)
    if(score >= max):
      max = score
      ret = p
  return ret


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
      p = game.puttableMonteCarloTreeSearch(board, player, 500)
      #p = puttableNN(board, player)
    else:
      p = puttableNN(board, player)
      #p = game.puttableMonteCarloTreeSearch(board, player, 100)
      #p = game.puttableRandom(board, player)
    
    if(p is None):
      player = -player
      history.append(numpy.append(player, (board.ravel())))
      if(not game.canPut(board, player)):
        break
      continue
    
    #print("player",player, "put",p)
    board = game.put(board, player, p)
    player = -player
    
    history.append(numpy.append(player, (board.ravel())))
    
    game.printBoard(board)
  
  win = game.judge(board)
  #print("win:", win)
  return numpy.vstack(history).astype(float), numpy.vstack([[win]]*len(history)).astype(float)
