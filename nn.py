#!/usr/bin/env python

import tensorflow as tf
import os.path
import random_play
import numpy
import time

class NeuralNet:
  def __init__(self):
    # input (player, board...)
    self.x = tf.placeholder(tf.float32, [None, 65], name="X")
    # output winner(-1,0,1)
    self.y_ = tf.placeholder(tf.float32, [None, 1], name="y_")

    h_unit_num = 512
    W1 = tf.Variable(tf.truncated_normal([65, h_unit_num], stddev=0.1), name="W1")
    b1 = tf.Variable(tf.zeros([h_unit_num]), name="b1")
    h = tf.nn.relu(tf.matmul(self.x, W1) + b1)

    W2 = tf.Variable(tf.truncated_normal([h_unit_num, 1], stddev=0.1), name="W2")
    b2 = tf.Variable(tf.zeros([1]), name="b2")

    self.y = tf.matmul(h, W2) + b2

    self.l2loss = tf.nn.l2_loss(self.y_-self.y)
    self.train_step = tf.train.AdamOptimizer(1e-4).minimize(self.l2loss)

    self.saver = tf.train.Saver()
    
    self.sess = tf.Session()
    #initialize
    if os.path.exists("./variables.ckpt"):
      print("restore")
      self.saver.restore(self.sess, "./variables.ckpt")
    else:
      print("init")
      self.sess.run(tf.initialize_all_variables())
  
  def evaluate(self, data):
    return self.sess.run(self.y, feed_dict={self.x: data})
  
  def train(self, inputs, labels):
    return self.sess.run(self.train_step, feed_dict={self.x:inputs, self.y_: labels})
  
  def loss(self, inputs, labels):
    return self.sess.run(self.l2loss, feed_dict={self.x:inputs, self.y_: labels})
  
  def save(self):
    self.saver.save(self.sess, "./variables.ckpt")
  
  def __del__(self):
    self.sess.close()

neuralNet = NeuralNet()