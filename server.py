#!/usr/bin/env python

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("Hello, world")

def make_app():
  return tornado.web.Application([
    (r"/(.*)", tornado.web.StaticFileHandler,
      {"path": "www", "default_filename": "index.html"})
  ])


if __name__ == "__main__":
  app = make_app()
  app.listen(8888)
  tornado.ioloop.IOLoop.current().start()
