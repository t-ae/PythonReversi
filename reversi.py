#!/usr/bin/env python

import numpy
import random

# board 8x8 int array
# black=1 white=-1

class Game:
  def __init__(self):
    self.__empty = 0
    self.__black = 1
    self.__white = -1
    
    self.__range = [0,1,2,3,4,5,6,7]
    self.__positions = [(x,y) for x in self.__range for y in self.__range]
    self.__ds = [(dx, dy) for dx in [0,-1,1] for dy in [0,-1,1]][1:]
  
  def createBoard(self):
    board = numpy.zeros([8,8], dtype=int)
    board[3,3] = self.__black
    board[4,4] = self.__black
    board[3,4] = self.__white
    board[4,3] = self.__white
    return board
  
  def printBoard(self, board):
    for y in range(-1,8):
      for x in range(-1, 8):
        if(x==-1 and y == -1):
          print(" ", end="")
        elif(x==-1):
          print("ABCDEFGH"[y], end="")
        elif(y==-1):
          print(" "+"12345678"[x], end="")
        elif(board[x,y]==1):
          print(" X", end="")
        elif(board[x,y]==-1):
          print(" O", end="")
        else:
          print(" .", end="")
      print("")
  
  # bools
  def isInBoard(self, position):
    return 0<=position[0] and position[0]<8 and 0<=position[1] and position[1]<8
  
  def canPut(self, board, player = None, position = None):
    if(player is None):
      return self.canPut(board, __black) or self.canPut(board, __white)
    elif(position is None):
      for pos in self.__positions:
        if self.canPut(board, player, pos):
          return True
      return False
    elif(not self.isInBoard(position) or board[position]!=self.__empty):
      return False
    else:
      for ds in self.__ds:
        if(self.__canPutSub(board, player, position, ds)):
          return True
      return False
  
  def __canPutSub(self, board, player, position, ds, r = False):
    nowPos = (position[0] + ds[0], position[1] + ds[1])
    if(not self.isInBoard(nowPos)):
      return False
    if(board[nowPos] == self.__empty):
      return False
    elif(board[nowPos] == player):
      return r
    else:
      return self.__canPutSub(board, player, nowPos, ds, True)
  
  # return board(numpy.ndarray)
  def put(self, board, player, position):
    board = numpy.copy(board)
    if(board[position] != self.__empty):
      raise Exception("Try to put invalid place.")
    board[position] = player
    for ds in self.__ds:
      self.__putSub(board, player, position, ds)
    return board
  
  def __putSub(self, board, player, position, ds):
    nowPos = (position[0] + ds[0], position[1] + ds[1])
    if(not self.isInBoard(nowPos)):
      return False
    elif(board[nowPos]==self.__empty):
      return False
    elif(board[nowPos] == player):
      return True
    elif(self.__putSub(board, player, nowPos, ds)):
      board[nowPos] = player
      return True
    else:
      return False
  
  def judge(self, board):
    s = numpy.sum(board)
    if(s>0):
      return self.__black
    elif(s<0):
      return self.__white
    else:
      return self.__empty
  
  def puttables(self, board, player):
    puttables = []
    for pos in self.__positions:
      if(self.canPut(board, player, pos)):
        puttables.append(pos)
    return puttables
  
  def puttableRandom(self, board, player):
    xx = [0,1,2,3,4,5,6,7]
    yy = [0,1,2,3,4,5,6,7]
    random.shuffle(xx)
    random.shuffle(yy)
    for pos in [(x,y) for x in xx for y in yy]:
      if(self.canPut(board, player, pos)):
        return pos
    return None
  
  def puttableMonteCarloTreeSearch(self, board, player, playoutNum = 100, maxdepth=-1):
    rootNode = self._Node(self, None, board, player, maxdepth)
    for i in range(playoutNum):
      node = rootNode
      
      while(len(node.puttables) == 0 and len(node.children)>0):
        node = node.selectNode()
      
      if(len(node.puttables)>0):
        node = node.expandChild()
      
      #node.printRoute()
      node.playout()
    rootNode.dump()
    return rootNode.selectMove()
  
  def puttableInput(self, board, player):
    print("you are ","X" if player==1 else "O")
    self.printBoard(board)
    while(True):
      s = input("input position (ex. A3):")
      if(len(s) == 2):
        y = "ABCDEFGH".find(s[0])
        x = "12345678".find(s[1])
        if(0<=x and x<8 and 0<=y and y<8):
          if(self.canPut(board, player, (x,y))):
            return (x,y)
    
  
  def playout(self, board, player):
    board = numpy.copy(board)
    while(True):
      p = self.puttableRandom(board, player)
      if(p is None):
        player = -player
        if(not self.canPut(board, player)):
          break
        continue
      board = self.put(board, player, p)
      player = -player
    return self.judge(board)
  
  
  
  class _Node:
    def __init__(self, game,  parent, board, player, maxdepth=-1, move = None):
      self.game = game
      self.parent = parent
      
      self.board = board
      self.player = player
      
      self.move = move
      self.maxdepth = maxdepth
      
      if(maxdepth==0):
        self.puttables=[]
      else:
        self.puttables = game.puttables(self.board, self.player)
        if(len(self.puttables) == 0):
          player = -player
          self.puttables = game.puttables(self.board, self.player)
      
      self.children = []
      
      # number of wins of oppent(=-self.player)
      self.opponentTotalWins = 0
      self.totalPlayouts = 0
    
    def expandChild(self):
      random.shuffle(self.puttables)
      p = self.puttables.pop()
      b = self.game.put(self.board, self.player, p)
      child = self.game._Node(self.game, self, b, -self.player, self.maxdepth-1, p)
      self.children.append(child)
      return child
    
    def selectNode(self):
      max = -9999
      ret = None
      for child in self.children:
        ucb = self.ucb(child)
        if(max <= ucb):
          max = ucb
          ret = child
      return ret
    
    def selectMove(self):
      if(not self.parent is None):
        raise Exception("selectMove is only for rootNode.")
      if(len(self.children)==0 and len(self.puttables)==0):
        return None
      else:
        ret = None
        max = -10000
        for c in self.children:
          score = c.opponentTotalWins / c.totalPlayouts
          if(score >= max):
            ret = c
            max = score
        return ret.move
    
    def ucb(self, child):
      return child.opponentTotalWins / child.totalPlayouts \
        + numpy.sqrt(2*self.totalPlayouts / child.totalPlayouts)
    
    def playout(self):
      win = self.game.playout(self.board, self.player)
      self.backpropagate(win)
    
    def backpropagate(self, win):
      node = self
      while(not node is None):
        if(node.player == -win):
          node.opponentTotalWins += 1
        node.totalPlayouts += 1
        node = node.parent
    
    def getRootNode(self):
      node = self
      while(not node.parent is None):
        node = node.parent
      return node
    
    def printRoute(self):
      node = self
      while(not node.parent is None):
        print(node.move, end="<-")
        node = node.parent
      print("")
    
    def dump(self, ucb=0, pad=0):
      print(" "*pad, end="")
      print(self.move, self.player, ucb, self.opponentTotalWins, self.totalPlayouts, self.maxdepth)
      for c in self.children:
        u = self.ucb(c)
        c.dump(u,pad+2)


game = Game()