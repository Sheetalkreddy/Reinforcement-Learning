# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 11:22:41 2017

@author: cindy
"""

#player desc
#picks a move from available moves uniformly at random

import random

class silly:
    
    
    def get_move(self, state, reward, position): #assumes a valid state,no final state
        available_moves = []
        num_players = len(state)
        if state[position]>0: #if player's heap has coins
            available_moves.append([1,-1]) #picks only from his heap
            for p in range(num_players):
                if (p!=position and state[p]>0):
                    available_moves.append([1,p]) #picks from his heap and another player's heap
        else:  #if player's heap has no coins
            for p in range(num_players):
                if state[p]>0:
                    available_moves.append([0,p]) #picks only from another player's heap
        return random.sample(available_moves,1)[0]          
            
        
            
    def end_game(self, reward):
        None