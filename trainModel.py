import numpy as np
from alexnet import alexnet, conv_net
import tensorflow as tf

WIDTH = 80
HEIGHT = 36
LR = 1e-3
EPOCHS = 2
MODEL_NAME = 'models/track-mania-self-driving-small-ne.model'
model = conv_net(WIDTH, HEIGHT, LR)

train_data = np.load('data/newDataBinary.npy')

train = train_data[:-6000]
test = train_data[-6000:]

X = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,1)
Y = [i[1] for i in train]

test_x = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,1)
test_y = [i[1] for i in test]
model.fit({'input': X}, {'targets': Y}, n_epoch=EPOCHS, validation_set=({'input': test_x}, {'targets': test_y}), 
    snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

# tensorboard --logdir=foo:C:/Users/Turic/Documents/Zavrsni/log

model.save(MODEL_NAME)
