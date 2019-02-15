import os
os.environ['KERAS_BACKEND']='theano'
import random
import numpy as np

from keras.models import model_from_json, Model
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten


class Player_Agent():

    def __init__(self):

        self.model = self.create_model()


    def create_model(self):

        model = Sequential()
        model.add(Dense(50, input_dim = 9,activation='relu'))
        model.add(Dense(50,activation = 'relu'))

        model.add(Dense(9))

        model.compile(optimizer='sgd',loss='mse')

        return model

    def train_model(self,inputs,targets,batch_size = 1):
        return  self.model.train_on_batch(inputs, targets )

    def make_move(self,state,epi = 0.4,max_moves = 9):
        if (random.random()<epi):
            return random.randint(0,max_moves-1)
        else:
            Q_s = self.model.predict(state.reshape(1,9),batch_size = 1)
            return np.argmax(Q_s[0])
