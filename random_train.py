#!/usr/bin/env python

import random_play
import reversi

player = 1

for i in range(1000):
  xs,ys = random_play.playRandomlyUnfair(player)
  random_play.nn.neuralNet.train(xs, ys)
  print("step:",i,"loss:",random_play.nn.neuralNet.loss(xs, ys))
  player = -player
  

random_play.nn.neuralNet.save()