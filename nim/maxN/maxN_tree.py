# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 13:43:18 2017

@author: cindy
"""

import math
import random


class node: #takes initial state, starting player and constructs the tree
    def __init__(self, state, player): #root will store a dict of all nodes
        self.state = state
        self.player = player #player who can make a move from this state
        self.num_players = len(state)
        self.children = []
        self.get_children()
        self.payoff = [0 for i in range(self.num_players)]
        #self.best_child is the best child (object address) to go to from a node
        self.get_payoff()
        
        
            
    def get_children(self):
        if self.state[self.player]==0: #no coins in player's heap
            for i in range(self.num_players):
                if self.state[i]>0:
                    new_state = [c for c in self.state]
                    new_state[i] = new_state[i] - 1
                    self.children.append(node(new_state,(self.player+1)%self.num_players))
        else:   #players heap has coins
            new_state = [c for c in self.state]
            new_state[self.player] = new_state[self.player] - 1
            self.children.append(node(new_state, (self.player+1)%self.num_players)) #pick only from your heap
            other_players = list(range(self.num_players))
            other_players.remove(self.player)
            for i in other_players:         #pick from your heap and anybody else's heap
                if self.state[i]>0:
                    new_state = [c for c in self.state]
                    new_state[self.player] = new_state[self.player] - 1
                    new_state[i] = new_state[i] - 1
                    self.children.append(node(new_state, (self.player+1)%self.num_players))
            
                    
    def get_payoff(self): 
        if not self.children:  #if final state
            winner = (self.player-1)%self.num_players
            self.payoff[winner] = 1
        else:
            best_payoffs = [[-1 for i in range(self.num_players)]] #each element is a payoff vector
            best_children = [] #each element is the best child
            #best_payoffs: all have same payoff and rel payoff for player, and same variance among other players
            for child in self.children:
                cp = child.payoff[self.player]
                bp = best_payoffs[0][self.player]
                if cp>bp:
                    best_payoffs = [child.payoff]
                    best_children = [child]                    
                elif cp==bp: #see if you can make a choice here
                    bpsum = sum(best_payoffs[0])
                    cpsum = sum(child.payoff)
                    if bpsum!=0:
                        bprel = best_payoffs[0][self.player]/bpsum
                    else:
                        bprel = math.inf
                    if cpsum!=0:
                        cprel = child.payoff[self.player]/cpsum
                    else:
                        cprel = math.inf
                    if bprel<cprel:
                        best_payoffs = [child.payoff]
                        best_children = [child]
                    elif bprel==cprel:
                        other_players = list(range(self.num_players))
                        other_players.remove(self.player)
                        bpsum-=bp
                        cpsum-=bp
                        bpvar = sum([(best_payoffs[0][i]-bpsum)**2 for i in other_players])
                        cpvar = sum([(child.payoff[i]-bpsum)**2 for i in other_players])
                        if cpvar<bpvar:
                            best_payoffs = [child.payoff]
                            best_children = [child]
                        elif cpvar==bpvar:
                            best_payoffs.append(child.payoff)
                            best_children.append(child)
            r = random.randint(0,len(best_children)-1) #choose a child randomly from best children
            self.payoff = best_payoffs[r]
            self.best_child = best_children[r]
                
                       
    def print_tree(self, level=0):
        ret = " "*(self.num_players*3+2)*level+str(self.state)+str(self.player)+"\n"
        ret += " "*(self.num_players*3+2)*level+str(self.payoff)+"\n"
        for child in self.children:
            ret += child.print_tree(level+1)
        return ret
                    



if __name__ == "__main__":  
    init_state = [7,5]                  
    root = node(init_state, 0)
    print (root.print_tree()) #a node shows  state, next move player, num_wins for each player


