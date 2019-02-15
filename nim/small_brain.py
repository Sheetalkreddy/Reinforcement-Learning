# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 11:47:41 2017

@author: cindy
"""
#player description:
#1. obeys the rules
#2. if he has a winning move, he makes it.
#3. Chooses randomly from the moves that have P(next player wins)=0
#4. If all moves cause next player to win, randomly chooses any move

import random

class small_brain():
    
    def get_move(self, state, reward, position):       #assumes a valid state, no final state
        num_coins = sum(state)
        num_heaps = len(state)
        next_player = (position+1)%num_heaps
        my_coins = state[position]
        next_coins = state[next_player] #num of next players coins
        
        non_zero_heaps = [] #other heaps with non zero coins
        for i in range(num_heaps):
            if state[i]>0 and i!=position:
                non_zero_heaps.append(i) 
                
        if my_coins==0: #if player's heap has no coins
            if num_coins==1:
                return [0, non_zero_heaps[0]] #winning move
            if next_coins==2 and num_coins==3:
                if non_zero_heaps[0]==next_player:
                    return [0,non_zero_heaps[1]] #the other move allows next player to win
                return [0,non_zero_heaps[0]]
            return [0, random.choice(non_zero_heaps)] #all moves equivalent for him
        
        else: #players heap has coins
            if num_coins>4:
                return [1, random.choice(non_zero_heaps+[-1])] #all moves equivalent
            if num_coins==my_coins:
                return [1,-1] #only move
            if num_coins==2:
                return [1, non_zero_heaps[0]] #winning move
            if num_coins==3:
                if my_coins==2:
                    if non_zero_heaps[0]==next_player:
                        return [1, random.choice(non_zero_heaps+[-1])]
                    return [1, -1]
                #player has one coin
                if next_coins==2 or next_coins==0:
                    return [1, -1]
                return [1, random.choice(non_zero_heaps+[-1])]
            #num_coins=4 here
            if my_coins==3:
                return [1, random.choice(non_zero_heaps+[-1])]
            if my_coins==2:
                if next_coins==2:
                    return [1, -1]
                return [1, random.choice(non_zero_heaps+[-1])]
            #my_coins=1 here
            if next_coins==1:
                return [1, next_player]
            if next_coins==2:
                if non_zero_heaps[0]==next_player:
                    return [0,random.choice([non_zero_heaps[1],-1])] #the other move allows next player to win
                return [0,random.choice([non_zero_heaps[0],-1])]                                
            return [1, random.choice(non_zero_heaps+[-1])]
           
            
    def end_game(self, reward):
        None
                        
                    
                
            
            
            
                
                
                
        
                
        