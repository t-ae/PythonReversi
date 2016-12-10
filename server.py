#!/usr/bin/env python

import json, threading, os
from tornado import ioloop, web, websocket, httpserver
from keras.models import load_model
import reversi, player, neural_player

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.h5")
model = load_model(MODEL_PATH)

AI_RANDOM = "RANDOM"
AI_MTS = "MTS"
AI_NEURAL = "NEURAL"
AI_NEURAL_MTS = "NEURAL_MTS"

game = reversi.Game()

players = {
    AI_RANDOM: player.RandomUniform(),
    AI_MTS: player.RandomMTS(300, 3),
    AI_NEURAL: neural_player.Neural(model),
    AI_NEURAL_MTS: neural_player.NeuralMTS(100, 3)
}

class WSHandler(websocket.WebSocketHandler):
    __lock = threading.Lock()

    def open(self):
        print("new connection")
        self.nowPlayer = 1
        self.ai = AI_RANDOM
        self.initBoard(1)

    def on_message(self, message):
        with self.__lock:
            try:
                msg = json.loads(message)
                print(msg)
                if msg["command"] == "put":
                    pos = (msg["position"][0], msg["position"][1])
                    if game.canPut(self.board, -self.me, pos):
                        # client put
                        self.board = game.put(self.board, -self.me, pos)
                        self.nowPlayer = self.me
                        self.send_update()

                        # server put
                        self.serverPut()
                    else:
                        self.send_error("Can't put there.")
                elif msg["command"] == "ai":
                    self.ai = msg["ai"]
                    print("Set AI", self.ai)
                elif msg["command"] == "restart":
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
        self.board = game.createBoard()
        self.nowPlayer = 1

        self.send_update()

        if self.me == 1:
            # First hand
            self.serverPut()

    def serverPut(self):
        player = players[self.ai]
        if player == None:
            send_error("Invalid Player:", self.ai)
            return
        cell = player.select(game, self.board, self.me)
        if cell is None:
            # server pass
            if not game.canPut(self.board, -self.me):
                # client pass = end
                self.judge()
                return
            else:
                self.nowPlayer = -self.me
                return
        
        self.board = game.put(self.board, self.me, cell)

        if not game.canPut(self.board, -self.me):
            # client pass
            self.send_update()
            self.serverPut()
        else:
            self.nowPlayer = -self.me
            self.send_update()
    
    def send_update(self):
        b = self.board.ravel(order="F").astype(int).tolist()
        p = self.nowPlayer
        j = { "command":"update", "player":p, "board": b}
        self.write_message(j)
    
    def judge(self):
        win = game.judge(self.board)
        self.write_message({ "command":"judge", "winner": win})
        self.nowPlayer = self.me




def make_app():
    return web.Application([
        (r"/ws", WSHandler),
        (r"/(.*)", web.StaticFileHandler,
            {"path": os.path.dirname(__file__)+"/www", "default_filename": "index.html"}),
    ])


if __name__ == "__main__":
    app = make_app()
    http_server = httpserver.HTTPServer(app)
    print("http://127.0.0.1:8888")
    http_server.listen(8888)
    ioloop.IOLoop.current().start()
