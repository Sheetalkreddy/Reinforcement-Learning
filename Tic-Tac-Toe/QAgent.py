import os
os.environ['KERAS_BACKEND']='theano'
import random
import numpy as np
from Experince_Buffer import Experience_Replay_Buffer

from keras.models import model_from_json, Model
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten


class QAgent():

    def __init__(self,epi):

        self.model = self.create_model()
        self.expbuff = Experience_Replay_Buffer(10000)
        self.epi = epi

    def setEpi(self,new):
        self.epi = new

    def addMem(self,mem):
        self.expbuff.add(mem)

    def create_model(self):

        model = Sequential()
        model.add(Dense(50, input_dim = 9,activation='relu'))
        model.add(Dense(50,activation = 'relu'))

        model.add(Dense(9))

        model.compile(optimizer='adam',loss='mse')

        return model

    def train_model(self,batch_size = 1):
        inputs,targets = self.expbuff.buffer_get_batch(self.model,batch_size)
        return  self.model.train_on_batch(inputs, targets )

    def make_move(self,state,mode = 1,max_moves = 9):
        count = 0
        if (random.random()<self.epi):

            while count <1000:
                move = random.randint(0,max_moves-1)
                if state.reshape(9)[move] == 0:
                    return move,-1,None
            count+=1
        else:

            Q_s = self.model.predict(state.reshape(1,9),batch_size = 1)[0]
            for i in np.argsort(Q_s)[::-1]:
                if state.reshape(9)[i] == 0:

                    move = i
                    return move,Q_s[i],Q_s
    def __str__(self):
        return "QAgent"
