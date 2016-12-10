#!/usr/bin/env python

import os, glob, time
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Merge, Reshape, Flatten, InputLayer
from keras.layers.local import LocallyConnected2D
from keras.layers.pooling import MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import ELU
from keras.optimizers import Adam

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.h5")
RECORD_PATH = os.path.join(os.path.dirname(__file__), "./record/*.npz")

if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
else:
    board_model = Sequential([
        Reshape([8, 8, 1], input_shape=[8, 8], name="Reshape"),
        LocallyConnected2D(64, 3, 3, border_mode='valid', name="LC1"), # 6x6
        ELU(name="ELU1"),
        BatchNormalization(name="BN1"),
        LocallyConnected2D(256, 3, 3, border_mode='valid', name="LC2"), # 4x4
        ELU(name="ELU2"),
        BatchNormalization(name="BN2"),
        Flatten(name="Flatten")
    ])
    color_input = InputLayer([1])

    model = Sequential([
        Merge([board_model, color_input], mode="concat", name="MERGE"),
        Dense(512, name="Dense1"),
        ELU(name="ELU2_1"),
        Dense(128, name="Dense2"),
        ELU(name="ELU2_2"),
        Dense(3, activation="softmax", name="Dense3") # [DRAW, BLACK, WHITE]
    ])
    
    adam = Adam(lr=1e-6, beta_1=0.5)
    model.compile(optimizer="adam", 
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])

records = glob.glob(RECORD_PATH)
print("{0} records".format(len(records)))

for i in range(1, 99999999):
    print("\nepoch:", i)
    np.random.shuffle(records)
    for j, record in enumerate(records):
        npz = np.load(record)
        X_board = npz["X_board"]
        X_color = npz["X_color"]
        y = npz["y"]
        y_ = np.concatenate([y.reshape([1, 3])]*len(X_color), axis=0)

        loss, acc = model.train_on_batch([X_board, X_color], y_)
        if j%10==0:
            print("{0}: loss: {1:3.5f}, acc: {2:3.5f}".format(y, loss, acc),end='\r')
    
    model.save(MODEL_PATH)
    time.sleep(0.5)