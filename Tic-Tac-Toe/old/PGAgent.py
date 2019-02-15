import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.autograd as autograd
from torch.autograd import Variable




class Policy(nn.Module):
    def __init__(self):
        super(Policy, self).__init__()
        self.affine1 = nn.Linear(9, 128)
        self.affine2 = nn.Linear(128,9)

        self.saved_actions = []
        self.rewards = []

    def forward(self, x):
        x = F.relu(self.affine1(x))
        action_scores = self.affine2(x)
        return F.softmax(action_scores)


class PGAgent():

    def __init__(self):

        self.policy = Policy()
        self.optimizer = optim.Adam(self.policy.parameters(), lr=1e-2)

        self.epoch=0
        self.episodeReward = 0
        self.gamma = 0.99
        self.movesMade = 0
    def train_model(self,inputs,targets,batch_size = 1):
        return  self.model.train_on_batch(inputs, targets )

    def make_move(self,st,epi = 0.4,max_moves = 9):
        state = np.copy(st.reshape(9))
        state = torch.from_numpy(state).float().unsqueeze(0)
        probs = self.policy(Variable(state))
        action = probs.multinomial()
        self.policy.saved_actions.append(action)
        return action.data[0,0]

    def getreward(self,reward):
        self.policy.rewards.append(reward)

    def finish_episode(self):
        R = 0
        rewards = []
        for r in self.policy.rewards[::-1]:
            self.episodeReward +=r
            R = r + self.gamma * R
            rewards.insert(0, R)
        rewards = torch.Tensor(rewards)
        rewards = (rewards - rewards.mean()) / (rewards.std() + np.finfo(np.float32).eps)
        for action, r in zip(self.policy.saved_actions, rewards):
            action.reinforce(r)
        self.optimizer.zero_grad()
        autograd.backward(self.policy.saved_actions, [None for _ in self.policy.saved_actions])
        self.optimizer.step()
        del self.policy.rewards[:]
        del self.policy.saved_actions[:]



    def Train(self):
        self.epoch+=1

        self.finish_episode()
        print "Epoch:",self.epoch,"Reward:",self.episodeReward,"Moves Made:",self.movesMade
