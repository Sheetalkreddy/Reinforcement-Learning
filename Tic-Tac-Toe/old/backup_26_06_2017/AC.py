import os
os.environ['KERAS_BACKEND']='tensorflow'
from keras.models import Model,Sequential
from keras.layers.core import Dense
from keras.optimizers import Adagrad

from keras import layers
from keras import backend as K
from keras import utils as np_utils
from keras import optimizers

import numpy as np
import random


class PGAgent():

    def __init__(self,epi = 0.3,gamma = 0.99):

        self.model = self.createModel(9,9)
        self.epi = epi
        self.gamma = gamma
        self.epoch = 0




        self.__train_func()
        # print 'here'



    def make_move(self,state):



        # if random.random() < self.epi:
        #     seq = random.sample(range(9),9)
        #     for move in seq:
        #         if state[move] == 0:
        #             return move


        inp = state.reshape(1,state.shape[0])
        QValues = self.model.predict(inp,batch_size = 1)[0]
        # print QValues
        move = np.random.choice(np.arange(9), p=QValues)
        # print 'AC Agent:',move
        return move




    def setepi(self,new):
        self.epi = new


    def discounted_r(self,epi_reward):
        discounted_r = np.zeros_like(np.array(epi_reward),dtype = 'float32')
        total_reward = 0
        running_add = 0
        for t in reversed(range(len(epi_reward))):
            total_reward += epi_reward[t]
            running_add = running_add * self.gamma + epi_reward[t]
            discounted_r[t] = running_add
        discounted_r -= discounted_r.mean() 
        discounted_r /= discounted_r.std()
        return total_reward,discounted_r



    def __train_func(self):
        action_prob_placeholder = self.model.output
        action_onehot_placeholder = K.placeholder(shape=(None, 9),name="action_onehot")
        discount_reward_placeholder = K.placeholder(shape=(None,),name="discount_reward")
        action_prob = K.sum(action_prob_placeholder * action_onehot_placeholder, axis=1)
        log_action_prob = K.log(action_prob)
        loss = -1* log_action_prob * discount_reward_placeholder
        loss2= loss 
        loss = K.mean(loss)

        adam = optimizers.Adam()

        updates = adam.get_updates(params=self.model.trainable_weights,constraints=[],loss=loss)
        self.train_fn = K.function(inputs=[self.model.input,action_onehot_placeholder,discount_reward_placeholder],outputs=[loss,loss2],updates=updates)


    def Train(self,epi_states,epi_actions,epi_reward):
        self.epoch+=1
        action_onehot = np_utils.to_categorical(np.array(epi_actions), num_classes=9)
        # print action_onehot
        total_reward,discount_reward = self.discounted_r(epi_reward)
        # print len(epi_reward),len(epi_states),len(epi_actions)
        loss= self.train_fn([np.array(epi_states), action_onehot, discount_reward])
        # print a
        # print b
        print loss
        return loss
        # print "Epoch is:",self.epoch,"Reward is:",total_reward





    def createModel(self,InputSize,OutputSize):
        #model = Sequential()
        model = Sequential()
        model.add(Dense(150, activation='tanh', input_dim=InputSize))
        model.add(Dense(50, activation='tanh'))
        model.add(Dense(OutputSize,activation = 'softmax'))
        model.summary()
        #model.compile("adam","mse")

        return model

    def reset(self):
        self.state = np.ones(self.nbCards)
        if self.train == True:
            # print len(self.epi_reward)
            self.Train()
            # self.epi_reward = []
            # self.epi_states = []
            # self.epi_actions = []
