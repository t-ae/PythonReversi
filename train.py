#!/usr/bin/env python

import tensorflow as tf
import os.path
import random_play
import numpy
import time

# input (player, board...)
x = tf.placeholder(tf.float32, [None, 65], name="X")
# output winner(-1,0,1)
y_ = tf.placeholder(tf.float32, [None, 1], name="y_")

h_unit_num = 512
W1 = tf.Variable(tf.truncated_normal([65, h_unit_num], stddev=0.1), name="W1")
b1 = tf.Variable(tf.zeros([h_unit_num]), name="b1")
h = tf.nn.relu(tf.matmul(x, W1) + b1)

W2 = tf.Variable(tf.truncated_normal([h_unit_num, 1], stddev=0.1), name="W2")
b2 = tf.Variable(tf.zeros([1]), name="b2")

y = tf.matmul(h, W2) + b2

loss = tf.nn.l2_loss(y_-y)
train_step = tf.train.AdamOptimizer(1e-4).minimize(loss)

saver = tf.train.Saver()
with tf.Session() as sess:

  #initialize
  if os.path.exists("./variables.ckpt"):
    print("restore")
    saver.restore(sess, "./variables.ckpt")
  else:
    print("init")
    sess.run(tf.initialize_all_variables())
  
  stronger = 1
  
  for i in range(100):
    start = time.time()
    game, label = random_play.playRandomlyUnfair(stronger)
    #game, label = random_play.playMonteCarlo(10)
    sess.run(train_step, feed_dict={x: game, y_: label})
    print("step:",i,"loss:",sess.run(loss, feed_dict={x: game, y_: label}))
    print("time", time.time()-start)
    stronger = -stronger
  
  #save
  print("save")
  saver.save(sess, "./variables.ckpt")
  
  
  game, label = random_play.playRandomly()
  yy, l = sess.run([y, loss], feed_dict={x: game, y_: label})
  print("loss:",l)
  for i in range(len(label)):
    print("player:",game[i,0], "win", label[i], "y:", yy[i])
    print(numpy.reshape(game[i,1:], [8,8]))