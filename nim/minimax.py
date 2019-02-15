# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 07:47:27 2017

@author: cindy
"""

#player desc:
#makes his best move assuming other players to make his worst move

import minimax_tree as tree

class minimax:
    
    def __init__(self):
        self.in_game = 0
        
    def get_move(self, state, reward, position): 
        if not self.in_game: #construct new tree if new game is started
            self.root = tree.node(state, position) 
            new_state = self.root.best_child.state
            return minimax.find_move(new_state, state, position)          
        else: #otherwise, use the already constructed tree
            num_levels = len(state)-1 #levels to go down the tree
            next_level = [self.root]
            for i in range(num_levels):
                prev_level = next_level.copy()
                next_level = []
                for n in prev_level:
                    next_level += n.children
            #next_level now contains all possible states
            for n in next_level:
                if n.state==state:
                    self.root = n
                    break
            new_state = self.root.best_child.state
            return minimax.find_move(new_state, state, position)
       
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