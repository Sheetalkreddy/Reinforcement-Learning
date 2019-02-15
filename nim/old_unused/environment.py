# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 12:25:54 2017

@author: cindy
"""

import random

#two player game, variable number of heaps and coins
class nim():    
    def __init__(self, num_heaps = 2, num_coins = [20,15], win_reward = 1, invalid_reward = -2):
      self.num_heaps = num_heaps
      self.num_players = num_heaps
      self.num_coins = num_coins
      self.win_reward = win_reward
      self.invalid_reward = invalid_reward
      self.done = False
      
    def reset(self, num_heaps = 2, num_coins = [20,15]):
        self.num_heaps = num_heaps
        self.num_coins = num_coins
        self.done = False
        
    def check_win(self): #after making a move
        if sum(self.num_coins)==0:
            return 1            #return 1 if w0n, 0 if lost
        return 0
    
    def make_move(self,move): #move is a list like num_coins
        move_made = [(i,move[i]) for i in range(len(move)) if move[i]>0]
        if len(move_made)==1:
            if (move_made[0][1] <= self.num_coins[move_made[0][0]]):
                self.num_coins[move_made[0][0]] = move_made[0][1]
                return 1
        return 0
    
    def get_state(self):
        return self.num_coins
    
    def act(self,move):
        if self.make_move(move)==1:
            win = self.check_win()
            if win==1:
                self.done = True
                return (self.get_state, self.win_reward)
            else:
                return (self.get_state, 0) 
        else:
            self.done = True
            return (self.get_state, self.invalid_reward)
        
        
        
        
def one_game(agent1, agent2, num_heaps = 2, num_coins = [20,15], win_reward = 1, invalid_reward = -2):
    game = nim(num_heaps, num_coins, win_reward, invalid_reward)
    first = random.randint(0,1)
    if first==0:
        first_player = agent1
        second_player = agent2
    else:
        first_player = agent2
        second_player = agent1
    first_player.
    

        
    
    
            
    
        
            
    
        