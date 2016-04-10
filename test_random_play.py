#!/usr/bin/env python

import random_play
import reversi

player = 1
total = 10
correct = 0
for i in range(total):
  xs, ys = random_play.playRandomlyUnfair(player)
  if(ys[0] == player):
    correct += 1
  player = -player

print("stronger's win rate: ", correct, "/", total)