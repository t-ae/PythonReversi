#!/usr/bin/env python

import random_play
import reversi

player = 1
total = 10
correct = 0
for i in range(total):
  player = -player
  xs, ys = random_play.playRandomlyUnfair(player)
  if(ys[0] == player):
    correct += 1

print(correct / total)