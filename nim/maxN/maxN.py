# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 16:50:29 2017

@author: cindy
"""

#player desc:
#uses the maxN strategy 
#that is assumes other players make their best move and makes his best move


from maxN import maxN_tree as tree

class maxN():
    
    def __init__(self):
        self.in_game = 0
        
    def get_move(self, state, reward, position): 
        if not self.in_game:
            root = tree.node(state, position) 
            new_state = root.best_child.state
            return maxN.find_move(new_state, state, position)          
        else: #modify this part to use info from above tree, check if time reduces
            root = tree.node(state, position) 
            new_state = root.best_child.state
            return maxN.find_move(new_state, state, position)
       
    @staticmethod
    def find_move(new_state, state, position):
        if new_state[position]==state[position]:
                myheap = 0
        else:
                myheap = 1
        num_players = len(state)
        for i in range(num_players):
            if i!=position and new_state[i]!=state[i]:
                return [myheap, i]
        return [myheap, -1]
        
                
    def end_game(self, reward):
        self.in_game = 0