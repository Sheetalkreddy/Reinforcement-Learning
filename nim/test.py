# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 10:14:38 2017

@author: cindy
"""
import minimax_tree as tree

class mm():
    
    def __init__(self):
        self.in_game = 0
        
    def get_move(self, state, reward, position): 
            #construct new tree if new game is started
            self.root = tree.node(state, position) 
            new_state = self.root.best_child.state
            return mm.find_move(new_state, state, position)          

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
        
        
        

    