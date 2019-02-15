import numpy as np
from Random_Player import Random_Player
from Safe_Player import Safe_Player
from QAgent import QAgent

import random
class tictactoe():


    def __init__(self,winReward = 1,drawReward = -0.3,noResultReward = 0,InvalidReward = -2):
        self.board = np.zeros((3,3))
        self.done = False
        self.x = 1 #X Always goes first
        self.o = 2 #O Always goes second
        self.winReward = winReward
        self.drawReward = drawReward
        self.noResultReward = noResultReward
        self.InvalidReward = InvalidReward

    def reset(self):
        self.board = np.zeros((3,3))
        self.done = False

    def check_win(self,player):
        #Player is 1 for x and 2 for o
        board_state = np.where(self.board == player) # All the locations this player has played
        a,row_counts = np.unique(board_state[0],return_counts = True )
        a,col_counts = np.unique(board_state[1],return_counts = True )

        if (3 in row_counts) or (3 in col_counts):
            self.done = True
            return 1

        dig_1_count = 0
        dig_2_count = 0

        for i in range(self.board.shape[0]):
            if self.board[i,i] == player:
                dig_1_count+=1
            if self.board[i,2-i] == player:
                dig_2_count+=1
        if (dig_1_count == 3) or (dig_2_count == 3):
            self.done = True
            return 1

        return 0
    def make_move(self,move,player):
        #Player is 1 for X and 2 for O
        row = move/3
        col = move%3

        if self.board[row,col] == 0:
            self.board[row,col] = player
            return 1
        else:
            return -1

    def act(self,move,player):
        #Player is 1 if x and 2 if o
        if (self.make_move(move,player) == 1):
            win = self.check_win(player)
            if win == 1:
                return (self.get_state(),self.winReward)
            if win == 0:
                # Write check block here
                if np.count_nonzero(self.board) == 9:
                    self.done = True
                    return (self.get_state(),self.drawReward) # Draw

        else:
            self.done = True
            return (self.get_state(),self.InvalidReward)
        return (self.get_state(),self.noResultReward)

    def get_state(self):
        return [np.copy(self.board.reshape(9,1)),self.done]

    def printBoard(self):
        for i in self.board:
            to_print = ''
            for j in i:
                if j == 1:
                    to_print+=' X '
                elif j == 2:
                    to_print+=' O '
                else:
                    to_print+=  ' - '
            print to_print
            print

if __name__ == "__main__":

    winReward = 1
    loseReward = -1
    drawReward = 0
    invalidReward = -2
    noActionReward = 0

    env = tictactoe(winReward,drawReward,noActionReward,invalidReward)
    epochs = 100000
    testGames = 1000
    verbose = 0
    testverbose =3


    total_wins =[0,0]
    total_draws = [0,0]
    total_invalids =[0,0]
    total_losses = [0,0]
    batch_size = 32

    epi = 1
    epi_decay = 0.1
    epi_decay_interval = 15000
    epi_stop_thres = 0.5


    # p2 = Random_Player()
    p1 = QAgent(epi)
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

            if verbose >=2:
                env.printBoard()

            mem1.append(env.get_state()[0]) # Adding st to X player

            if mode ==1:
                x_move,QValue,QValues = p1.make_move(env.get_state()[0],mode)#input("Enter Valid Move for X: ")
            else:
                x_move,QValue,QValues  = p2.make_move(env.get_state()[0],mode)
            mem1.append(x_move) # Adding action of X Player

            x_reward = env.act(x_move,1)[1]

            if verbose>=1:
                print "Move Made By X: ",x_move,"QValue is: ",QValue,"Reward Earned By X :",x_reward
                print QValues
            if np.count_nonzero(env.board) >1:
                mem2.append(env.get_state())
                epi_o_mem.append(mem2)

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

                mem1.append(x_reward)
                mem1.append(env.get_state())
                epi_x_mem.append(mem1)

                if x_reward == winReward:
                    epi_o_mem[-1][2] = loseReward
                elif x_reward == drawReward:
                    epi_o_mem[-1][2] = drawReward
                epi_o_mem[-1][3][1] = True
                break

            if verbose>=2:
                env.printBoard()
            mem2 = [] #Memory of O Player

            mem2.append(env.get_state()[0])
            if mode == 1:
                o_move,QValue,QValues  = p2.make_move(env.get_state()[0],mode)
            else:
                o_move,QValue,QValues  = p1.make_move(env.get_state()[0],mode)#input("Enter Valid Move for O: ")

            mem2.append(o_move)

            o_reward = env.act(o_move,2)[1]
            mem2.append(o_reward)
            if verbose>=1:
                print "Move Made By O: ",o_move,"QValue is: ",QValue,"Reward Earned By O: ",o_reward
                print QValues

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

                mem2.append(env.get_state())
                epi_o_mem.append(mem2)
                mem1.append(loseReward)
                mem1.append(env.get_state())
                epi_x_mem.append(mem1)
                break
            else:
                mem1.append(x_reward)
                mem1.append(env.get_state())
                epi_x_mem.append(mem1)

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
                x_move,QValue,QValues  = p1.make_move(env.get_state()[0],mode)#input("Enter Valid Move for X: ")
            else:
                x_move,QValue,QValues  = p2.make_move(env.get_state()[0],mode)

            x_reward = env.act(x_move,1)[1]

            if testverbose>=1:
                print "Move Made By X: ",x_move,"QValue is: ",QValue,"Reward Earned By X :",x_reward
                print QValues

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
                o_move,QValue,QValues  = p2.make_move(env.get_state()[0],mode)
            else:
                o_move,QValue,QValues  = p1.make_move(env.get_state()[0],mode)#input("Enter Valid Move for O: ")


            o_reward = env.act(o_move,2)[1]
            if testverbose>=1:
                print "Move Made By O: ",o_move,"QValue is: ",QValue,"Reward Earned By O: ",o_reward
                print QValues
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
