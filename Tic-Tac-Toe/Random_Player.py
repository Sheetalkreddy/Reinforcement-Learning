import random


class Random_Player():

    def make_move(self,state,mode= 1):

        while True:

            move = random.randint(0,8)

            if state.reshape(3,3)[move/3,move%3] == 0:
                return move,0,None

    def __str__(self):
        return "Random Player"
