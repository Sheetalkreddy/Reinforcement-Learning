import random
import numpy as np


class Experience_Replay_Buffer():

    def __init__(self,max_size):

        self.buff = []
        self.buff_size = max_size

    def add(self,memory):

        self.buff.append(memory)

        if len(self.buff) > self.buff_size:
            del self.buff[0]

    def show(self):

        for i in self.buff:
            print i[0][0].reshape(3,3),i[0][1],i[0][2],i[0][3].reshape(3,3)

    def buffer_get_batch(self,model,batch_size,nb_actions = 9,gamma = 0.9):
        size = min(batch_size,len(self.buff))

        inputs = np.zeros((size,9))
        targets = np.zeros((size,nb_actions))

        pop = random.sample(range(max(size,len(self.buff))),size)
        count = 0
        for i in pop:

            state_t = self.buff[i][0][0]
            state_tp1 = self.buff[i][0][3]
            reward = self.buff[i][0][2]
            action = self.buff[i][0][1]

            done = self.buff[i][1]

            inputs[count] = state_t.reshape(1,9)

            targets[count] = model.predict(inputs[count].reshape(1,9),batch_size = 1).reshape(1,9)

            Q_sa = model.predict(state_tp1.reshape(1,9),batch_size = 1   ).reshape(1,9)

            if done == True:
                targets[count,action] = reward
            else:
                targets[count,action] = reward - (gamma)*np.max(Q_sa[0])
            count+=1

        return inputs,targets
