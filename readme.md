# Python Reversi

## Requirement
- Keras(Tensorflow backend)
- numpy

## Run Server
Run `server.py`.
open http://127.0.0.1:8888/

## Create Records
Run `create_record.py`.
Records will be saved under `record` directory.

## Train with Records
Run `train_nn.py`.
Train with records under `record` directory.
Model will be saved to `model.h5`.

## Train with itself
Run `self_train.py`.
Two DNN players play, and train with result.