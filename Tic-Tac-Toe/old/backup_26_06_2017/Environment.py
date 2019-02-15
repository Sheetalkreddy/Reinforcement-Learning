import numpy as np


class Tic_Tac_Toe():

    def __init__(self):
        self.board = np.zeros((3,3))
        self.done = False
        self.player = 1
        self.ai = 2

    def reset(self):
        self.board = np.zeros((3,3))
        self.done = False


    def make_move(self,move,player):
        #Player is 1 for X and 2 for O
        row = move/3
        col = move%3

        if self.board[row,col] == 0:
            self.board[row,col] = player
            return 1
        else:
            return -1

    def check_win(self,player):
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

    def act(self,move,mode=1):

        # Mode is 1 if its players move
        # Mode is 2 if its ais move

        if mode == 1:

            if (self.make_move(move,self.player) == 1):
                # Valid make_move
                win = self.check_win(self.player)

                if win == 1:
                    return (self.get_state(),0.7)
                if win == 0:
                    # Write check block here
                    if np.count_nonzero(self.board) == 9:
                        self.done = True
                        return (self.get_state(),0.5) # Draw

            else:
                #Invalid move
                self.done = True
                return (self.get_state(),-1.0)

            return (self.get_state(),0)


        if mode == 2:

            if (self.make_move(move,self.ai) == 1):
                win = self.check_win(self.ai)
                if win == 1:
                    return (self.get_state(),-0.7)
                if win == 0:
                    # Write check block here
                    if np.count_nonzero(self.board) == 9:
                        self.done = True
                        return (self.get_state(),0.5) # Draw

            return (self.get_state(),0)






    def get_state(self):
        return (self.board.reshape(9,1),self.done)
