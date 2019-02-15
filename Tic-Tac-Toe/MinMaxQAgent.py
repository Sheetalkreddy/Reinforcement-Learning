import os
os.environ['KERAS_BACKEND']='theano'
import random
import numpy as np
from Experince_Buffer import Experience_Replay_Buffer

from keras.models import model_from_json, Model
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten


class MMQAgent():

    def __init__(self,epi):

        self.model = self.create_model()
        self.expbuff = Experience_Replay_Buffer(10000)
        self.epi = epi

    def setEpi(self,new):
        self.epi = new

    def addMem(self,mem):
        self.expbuff.add(mem)

    def create_model(self):

        model = Sequential()
        model.add(Dense(50, input_dim = 9,activation='relu'))
        model.add(Dense(50,activation = 'relu'))

        model.add(Dense(9))

        model.compile(optimizer='adam',loss='mse')

        return model

    def train_model(self,batch_size = 1):
        inputs,targets = self.expbuff.buffer_get_batch(self.model,batch_size)
        return  self.model.train_on_batch(inputs, targets )

    def make_move(self,state,mode = 1,max_moves = 9):
        count = 0
        if (random.random()<self.epi):

            while count <1000:
                move = random.randint(0,max_moves-1)
                if state.reshape(9)[move] == 0:
                    return move
            count+=1
        else:
            Q_s = self.model.predict(state.reshape(1,9),batch_size = 1)[0]
            if np.count_nonzero(state)%2==0:
                #Picking max move
                for i in np.argsort(Q_s)[::-1]:
                    if state.reshape(9)[i] == 0:
                        move = i
                        return move
            else:
                #Picking Min Move
                for i in np.argsort(Q_s):
                    if state.reshape(9)[i] == 0:
                        move = i
                        return move
    def __str__(self):
        return "QAgent"



if __name__ == "__main__":
    from environment import *
    from Random_Player import Random_Player
    from Safe_Player import Safe_Player
    from QAgent import QAgent
    winReward = 1
    loseReward = -1
    drawReward = 0
    invalidReward = -2
    noActionReward = 0

    env = tictactoe(winReward,drawReward,noActionReward,invalidReward)
    epochs = 200000
    testGames = 1000
    verbose = 0
    testverbose =0


    total_wins =[0,0]
    total_draws = [0,0]
    total_invalids =[0,0]
    total_losses = [0,0]
    batch_size = 32

    epi = 1
    epi_decay = 0.1
    epi_decay_interval = 20000
    epi_stop_thres = 0.5


    # p2 = Random_Player()
    p1 = MMQAgent(epi)
    p2 = p1#Random_Player()#Safe_Player()

    testPlayer =  Random_Player()

    for game in range(epochs):
        mode =  random.randint(1,2)


        if (game+1)%epi_decay_interval == 0:
            if epi-epi_decay>epi_stop_thres:
                epi-=epi_decay
                if str(p1) == "QAgent":
                    p1.setEpi(epi)
                elif str(p2) == "QAgent":
                    p2.setEpi(epi)

        if verbose >= 1:
            if mode == 1:
                print str(p1)+" is X and "+str(p2)+" is 0"

            else:
                print str(p2)+" is X and "+str(p1)+" is 0"
        epi_x_mem = []
        epi_o_mem = []
        while env.get_state()[1]==False:

            mem1= [] # Memory of X Player
            mem2 = [] #Memory of O Player

            if verbose >=2:
                env.printBoard()

            mem1.append(env.get_state()[0])
            if mode ==1:
                x_move = p1.make_move(env.get_state()[0],mode)#input("Enter Valid Move for X: ")
            else:
                x_move = p2.make_move(env.get_state()[0],mode)

            x_reward = env.act(x_move,1)[1]
            mem1.append(x_move)
            mem1.append(x_reward)
            mem1.append(env.get_state())
            epi_x_mem.append(mem1)
            if verbose>=1:
                print "Move Made By X: ",x_move,"Reward Earned By X :",x_reward


            if env.get_state()[1] == True:
                if verbose>=2:
                    env.printBoard()
                #X Wins the game
                if x_reward == winReward:
                    if mode == 1 :
                        total_wins[0]+=1
                        total_losses[1]+=1
                    else:
                        total_wins[1]+=1
                        total_losses[0]+=1

                elif x_reward == drawReward:
                    total_draws[0]+=1
                    total_draws[1]+=1



                if x_reward == winReward:
                    epi_o_mem[-1][2] = loseReward
                elif x_reward == drawReward:
                    epi_o_mem[-1][2] = drawReward
                epi_o_mem[-1][3][1] = True
                break

            if verbose>=2:
                env.printBoard()

            mem2.append(env.get_state()[0])
            if mode == 1:
                o_move = p2.make_move(env.get_state()[0],mode)
            else:
                o_move = p1.make_move(env.get_state()[0],mode)#input("Enter Valid Move for O: ")


            o_reward = env.act(o_move,2)[1]

            mem2.append(o_move)
            mem2.append(o_reward)
            mem2.append(env.get_state())
            epi_o_mem.append(mem2)
            if verbose>=1:
                print "Move Made By O: ",o_move,"Reward Earned By O: ",o_reward

            if env.get_state()[1] == True:
                if verbose>=2:
                    env.printBoard()
                #O Wins the game
                if o_reward == winReward:
                    if mode == 2 :
                        total_wins[0]+=1
                        total_losses[1]+=1
                    else:
                        total_wins[1]+=1
                        total_losses[0]+=1

                elif x_reward == drawReward:
                    total_draws[0]+=1
                    total_draws[1]+=1

                if o_reward == winReward:
                    epi_x_mem[-1][2] = loseReward
                elif o_reward == drawReward:
                    epi_x_mem[-1][2] = drawReward
                break


        for i in epi_x_mem:
            if str(p1) == "QAgent":
                p1.addMem(list(i))
            elif str(p2) == "QAgent":
                p2.addMem(list(i))

        for i in epi_o_mem:
            if str(p1) == "QAgent":
                p1.addMem(list(i))
            elif str(p2) == "QAgent":
                p2.addMem(list(i))

        if str(p1) == "QAgent":
            print "Epoch: ",str(game+1),"Loss:",p1.train_model(batch_size)
        elif str(p2) == "QAgent":
            print "Epoch: ",str(game+1),"Loss:",p2.train_model(batch_size)
        env.reset()

        if verbose>=3:
            print "X Memory:"
            for i in epi_x_mem:
                print i[0].reshape(1,9),i[1],i[2],i[3][0].reshape(1,9),i[3][1]
            print
            print "O Memory: "
            for i in epi_o_mem:
                print i[0].reshape(1,9),i[1],i[2],i[3][0].reshape(1,9),i[3][1]
            print

        print "Total Wins: ",total_wins,"Total Draws: ",total_draws,"Total Losses: ",total_losses,"Total Invalids: ",total_invalids,"Epi = ",p1.epi
















































    total_wins =[0,0]
    total_draws = [0,0]
    total_invalids =[0,0]
    total_losses = [0,0]
    batch_size = 32



    epi = 0
    if str(p1) == "QAgent":
        p1.setEpi(epi)
    elif str(p2) == "QAgent":
        p2.setEpi(epi)

    p2 =testPlayer #Safe_Player()



    for game in range(testGames):
        mode =  random.randint(1,2)




        if testverbose >= 1:
            if mode == 1:
                print str(p1)+" is X and "+str(p2)+" is 0"

            else:
                print str(p2)+" is X and "+str(p1)+" is 0"

        while env.get_state()[1]==False:


            if testverbose >=2:
                env.printBoard()


            if mode ==1:
                x_move = p1.make_move(env.get_state()[0],mode)#input("Enter Valid Move for X: ")
            else:
                x_move = p2.make_move(env.get_state()[0],mode)

            x_reward = env.act(x_move,1)[1]

            if testverbose>=1:
                print "Move Made By X: ",x_move,"Reward Earned By X :",x_reward


            if env.get_state()[1] == True:
                if testverbose>=2:
                    env.printBoard()
                #X Wins the game
                if x_reward == winReward:
                    if mode == 1 :
                        total_wins[0]+=1
                        total_losses[1]+=1
                    else:
                        total_wins[1]+=1
                        total_losses[0]+=1

                elif x_reward == drawReward:
                    total_draws[0]+=1
                    total_draws[1]+=1


                break

            if testverbose>=2:
                env.printBoard()

            if mode == 1:
                o_move = p2.make_move(env.get_state()[0],mode)
            else:
                o_move = p1.make_move(env.get_state()[0],mode)#input("Enter Valid Move for O: ")


            o_reward = env.act(o_move,2)[1]
            if testverbose>=1:
                print "Move Made By O: ",o_move,"Reward Earned By O: ",o_reward

            if env.get_state()[1] == True:
                if testverbose>=2:
                    env.printBoard()
                #O Wins the game
                if o_reward == winReward:
                    if mode == 2 :
                        total_wins[0]+=1
                        total_losses[1]+=1
                    else:
                        total_wins[1]+=1
                        total_losses[0]+=1

                elif x_reward == drawReward:
                    total_draws[0]+=1
                    total_draws[1]+=1


                break





        env.reset()


        print "Total Wins: ",total_wins,"Total Draws: ",total_draws,"Total Losses: ",total_losses,"Total Invalids: ",total_invalids,"Epi = ",p1.epi
