#!/usr/bin/env python

import numpy
import nn
import reversi

player = 1
b = reversi.game.createBoard()
data = numpy.append(player, b.ravel()).reshape([1,65])

print(nn.neuralNet.evaluate(data))
