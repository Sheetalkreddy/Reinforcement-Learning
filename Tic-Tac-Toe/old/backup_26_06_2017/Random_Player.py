import random


class Random_Player():

    def make_move(self,state):

        while True:

            move = random.randint(0,8)

            if state.reshape(3,3)[move/3,move%3] == 0:
                return move
