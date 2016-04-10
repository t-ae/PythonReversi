#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import reversi
import json
import threading
import numpy
import os.path

class WSHandler(tornado.websocket.WebSocketHandler):
  __lock = threading.Lock()
  
  def open(self):
    self.nowPlayer = 1
    self.initBoard(1)
    self.ai = "MTS"
  
  def on_message(self, message):
    with self.__lock:
      try:
        msg = json.loads(message)
        print(msg)
        if(msg["command"] == "put"):
          pos = (msg["position"][0], msg["position"][1])
          if(reversi.game.canPut(self.board, -self.me, pos)):
            # client put
            self.board = reversi.game.put(self.board, -self.me, pos)
            self.nowPlayer = self.me
            self.update()
            
            # server put
            self.serverPut()
          else:
            self.send_error("Can't put there.")
        elif(msg["command"] == "ai"):
          self.ai = msg["ai"]
          print("Set AI", self.ai)
        elif(msg["command"] == "restart"):
          self.initBoard(msg["side"])
          print("Restart", msg["side"])
        else:
          self.send_error("invalid command "+msg["command"])
      except (ValueError, KeyError):
        self.send_error("Failed to parse JSON.")
  
  
  def on_close(self):
    pass
  
  def send_error(self, message):
    self.write_message({"command":"error", "message":message})
  
  def initBoard(self, player):
    self.me = -player
    self.board = reversi.game.createBoard()
    self.nowPlayer = 1
    
    self.update()
    
    if(self.me == 1):
      # First hand
      self.serverPut()
  
  def selectedAi(self):
    if(self.ai=="MTS"):
      return lambda board, player: reversi.game.puttableMonteCarloTreeSearch(board, player, 300)
    #elif(self.ai=="NN"):
    #  def eval(board, player):
    #    puttables = reversi.game.puttables(board, player)
    #    print("candidate:", puttables)
    #    max = -10000
    #    ret = None
    #    for p in puttables:
    #      b = reversi.game.put(board, player, p)
    #      data = numpy.append(player, b.ravel()).astype(float).reshape([1,65])
    #      score = player*nn.neuralNet.evaluate(data)
    #      print("p:",p,"score:",score)
    #      if(score >= max):
    #        max = score
    #        ret = p
    #    return ret
    #        
    #  return eval
    else:
      return reversi.game.puttableRandom
  
  def serverPut(self):
    ai = self.selectedAi()
    pos = ai(self.board, self.me)
    if(pos is None):
      # server pass
      if(not reversi.game.canPut(self.board, -self.me)):
        # client pass
        self.judge()
        return
      else:
        self.nowPlayer = -self.me
        return
    self.board = reversi.game.put(self.board, self.me, pos)
    if(not reversi.game.canPut(self.board, -self.me)):
      # client pass
      self.update()
      self.serverPut()
    else:
      self.nowPlayer = -self.me
      self.update()
  
  def update(self):
    b = self.board.ravel(order="F").astype(int).tolist()
    p = self.nowPlayer
    j = { "command":"update", "player":p, "board": b}
    self.write_message(j)
  
  def judge(self):
    win = reversi.game.judge(self.board)
    self.write_message({ "command":"judge", "winner": win});
    self.nowPlayer = self.me




def make_app():
  return tornado.web.Application([
    (r"/ws", WSHandler),
    (r"/(.*)", tornado.web.StaticFileHandler,
      {"path": os.path.dirname(__file__)+"/www", "default_filename": "index.html"}),
  ])

if __name__ == "__main__":
  app = make_app()
  http_server = tornado.httpserver.HTTPServer(app)
  print("listening 8888...");
  http_server.listen(8888)
  tornado.ioloop.IOLoop.current().start()
