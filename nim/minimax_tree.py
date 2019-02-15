# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 13:43:18 2017

@author: cindy
"""
#constructs a multiplayer minimax tree for for_player 
#for the game of nim

import math
import random


class node: #takes initial state, starting player and constructs the tree
    def __init__(self, state, start_player, for_player=None, is_zerosum=False, state_node_dict=None): #root will store a dict of all nodes
        self.state = state
        self.player = start_player #player who can make a move from this state
        if for_player==None: #the minimax player
            self.for_player = start_player 
        else:
            self.for_player = for_player
        self.is_zerosum = is_zerosum
        if state_node_dict==None:#if root node
            self.state_node_dict={} #key is state and player
        else:
            self.state_node_dict=state_node_dict #every node has the reference to root node's dictionary
        self.num_players = len(state)
        self.children = []
        self.get_children()
        self.payoff = [0 for i in range(self.num_players)]
        #self.best_child is the best child (object address) to go to from a node
        self.get_payoff()
        
        
            
    def get_children(self):
        if self.state[self.player]==0: #no coins in player's heap
            for i in range(self.num_players): #pick only from other player's heap
                if self.state[i]>0:
                    new_state = [c for c in self.state]
                    new_state[i] = new_state[i] - 1
                    next_player = (self.player+1)%self.num_players
                    tuple_new_state = tuple(new_state+[next_player]) #last element is player    #tuple because list is unhashable
                    if tuple_new_state in self.state_node_dict: #if state,player combination already seen
                        self.children.append(self.state_node_dict[tuple_new_state])
                    else:
                        temp = node(new_state,next_player, self.for_player, self.is_zerosum, self.state_node_dict)
                        self.state_node_dict[tuple_new_state] = temp
                        self.children.append(temp)
                        
        else:   #players heap has coins
            new_state = [c for c in self.state]
            new_state[self.player] = new_state[self.player] - 1 #pick only from your heap
            next_player = (self.player+1)%self.num_players
            tuple_new_state = tuple(new_state+[next_player]) #last element is player    #tuple because list is unhashable
            if tuple_new_state in self.state_node_dict: #if state,player combination already seen
                self.children.append(self.state_node_dict[tuple_new_state])
            else:
                temp = node(new_state,next_player, self.for_player, self.is_zerosum, self.state_node_dict)
                self.state_node_dict[tuple_new_state] = temp
                self.children.append(temp)
             
            other_players = list(range(self.num_players))
            other_players.remove(self.player)
            for i in other_players:     #pick from your heap and anybody else's heap
                if self.state[i]>0:
                    new_state = [c for c in self.state]
                    new_state[self.player] = new_state[self.player] - 1
                    new_state[i] = new_state[i] - 1
                    next_player = (self.player+1)%self.num_players
                    tuple_new_state = tuple(new_state+[next_player]) #last element is player    #tuple because list is unhashable
                    if tuple_new_state in self.state_node_dict: #if state,player combination already seen
                        self.children.append(self.state_node_dict[tuple_new_state])
                    else:
                        temp = node(new_state,next_player, self.for_player, self.is_zerosum, self.state_node_dict)
                        self.state_node_dict[tuple_new_state] = temp
                        self.children.append(temp)
                    
            
                    
    def get_payoff(self): 
        if not self.children:  #if final state
            if self.is_zerosum:
                winner = (self.player-1)%self.num_players
                self.payoff[winner] = 1
                lose_reward = -1/(self.num_players-1) #distribute -1 among other players
                for p in range(self.num_players):
                    if p!=winner:
                        self.payoff[p] = lose_reward
            else:
                winner = (self.player-1)%self.num_players
                self.payoff[winner] = 1
        else:
            if self.player == self.for_player: #if it's the minimax player's turn
                self.get_best_move() #gets the best move for for_player
            else: #if it's some other player's turn
                self.get_worst_move() #gets the worst move for for_player
                
                
                
    def get_best_move(self): 
            best_payoffs = [[-100 for i in range(self.num_players)]] #each element is a payoff vector
            best_children = [] #each element is the best child
            #best_payoffs: all have same payoff for for_palyer
            for child in self.children:
                cp = child.payoff[self.player]
                bp = best_payoffs[0][self.player]
                if cp>bp:
                    best_payoffs = [child.payoff]
                    best_children = [child]                    
                elif cp==bp: 
                    best_payoffs.append(child.payoff)
                    best_children.append(child)
            r = random.randint(0,len(best_children)-1) #choose a child randomly from best children
            self.payoff = best_payoffs[r]
            self.best_child = best_children[r]
            
            
            
    def get_worst_move(self):
            worst_payoffs = [[100 for i in range(self.num_players)]] #each element is a payoff vector
            worst_children = [] #each element is a worst child
            #worst_payoffs: all have same payoff for for_player
            for child in self.children:
                cp = child.payoff[self.for_player]
                bp = worst_payoffs[0][self.for_player]
                if cp<bp:
                    worst_payoffs = [child.payoff]
                    worst_children = [child]                    
                elif cp==bp: 
                    worst_payoffs.append(child.payoff)
                    worst_children.append(child)
            r = random.randint(0,len(worst_children)-1) #choose a child randomly from the worst children
            self.payoff = worst_payoffs[r]
            self.best_child = worst_children[r]
                
                
                
                       
    def print_tree(self, level=0):
        ret = " "*(self.num_players*3+2)*level+str(self.state)+str(self.player)+"\n"
        ret += " "*(self.num_players*3+2)*level+str(self.payoff)+"\n"
        for child in self.children:
            ret += child.print_tree(level+1)
        return ret
                    



if __name__ == "__main__":  
    init_state = [2,2,2]                  
    root = node(init_state, 0, 1, False)
    print (root.print_tree()) #a node shows  state, next move player, minimax payoff for for_player


