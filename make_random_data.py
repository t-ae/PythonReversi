#!/usr/bin/env python

import random_play
import numpy
import time
X = []
Y = []

print("")
for i in range(100):
  start = time.time()
  x, y = random_play.playMonteCarlo(30)
  X.append(x)
  Y.append(y)
  elapsed_time = time.time() - start
  print(i,elapsed_time)

numpy.save("X.npy", numpy.vstack(X))
numpy.save("Y.npy", numpy.vstack(y))