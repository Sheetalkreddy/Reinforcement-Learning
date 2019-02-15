# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 01:32:08 2017

@author: cindy
"""

from small_brain import small_brain as sb
from minimax import minimax

from silly import silly
import matplotlib.pyplot as plt
import random
random.seed(1)

times = []
#players need to implement get_move and end_game functions.
def game(init_state, players, rep, win_reward, lose_reward): #atleast 2 players
    winner = [0]*rep
    num_players = len(players)
    for k in range(rep):
        print ("rep",k)
        next_player = -1 
        state = init_state[:]
        while sum(state)!=0:
            next_player = (next_player+1)%num_players
            move = players[next_player].get_move(state,0,next_player) #assume a valid move #reward 0 for intermediate states 
            state[next_player] -= move[0] #move[0] denotes if the player is picking a coin from his pile
            if move[1]!=-1:  #move[1] is -1 if not picking from other heaps
                state[move[1]]-=1 #remove a coin from some other player 
        for i in range(num_players): #this is just for final state and reward
            if i==next_player:
                players[i].end_game(win_reward) #final reward 1 for winner, -1 for others
            else:                           
                players[i].end_game(lose_reward)                
        winner[k] = next_player
    return winner

init_state = [5,5,5]    
players = [silly(), silly() , minimax()] 
rep = 100
winners =  game(init_state, players, rep,1,-1)

#print win percentages
print ("\nwin percentages:")
num_players = len(init_state)
for p in range(num_players):
    print (type(players[p]).__name__+": "+str(winners.count(p)*100/rep))



#plot winners
plt.scatter(range(rep),winners)
plt.ylabel("winner")
plt.xlabel("iteration")
