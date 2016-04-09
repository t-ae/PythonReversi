#!/usr/bin/env python

import nn
import random_play

for i in range(2):
  
  game, label = random_play.playRandomlyUnfair(1)
  nn.neuralNet.train(game, label)
  
  nn.neuralNet.save()
