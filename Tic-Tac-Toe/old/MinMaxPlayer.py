import numpy as np
import random

class min_max_player():


    def make_move(self,state):
        best = -1000

        empty = self.find_empty(state)

        if len(empty) == 9:
            return random.randint(0,8)
        best_move = -1
        for move in empty:

            new_board = np.copy(state)
            new_board[move] = 2 # Min Max Player
            value = self.minmax(new_board,0,False,player = 1)
            if best < value:
                best_move = move
                best = value

        return best_move

    def minmax(self,state,depth,isMaximisingPlayer,player):

        if self.check_win(state,player = 2):
            return 10-depth
        elif self.check_win(state,player = 1):
            return -10+depth
        elif self.check_terminal(state):
            return 0
        if isMaximisingPlayer:
            best_val = -1000
            empty_moves = self.find_empty(state)
            for move in empty_moves:

                new_board = np.copy(state)
                new_board[move] = player


                value = self.minmax(new_board,depth+1,False,player = 1)

                best_val = max(best_val,value)

            return best_val
        else:
            best_val = 1000
            empty_moves = self.find_empty(state)

            for move in empty_moves:

                new_board = np.copy(state)
                new_board[move] = player

                value = self.minmax(new_board,depth+1,True,player = 2)

                best_val = min(best_val,value)
            return best_val

    def find_empty(self,state):
        empty = []


        for i in range(9):
            if state[i] == 0:
                empty.append(i)

        return empty
    def check_terminal(self,state):
        if np.count_nonzero(state) == 9:
            return True
        else:
            return False
    def check_win(self,state,player = 1):
        board = state.reshape(3,3)
        ar = np.where(board == player)
        u, row_count = np.unique(ar[0], return_counts=True)
        u, col_count = np.unique(ar[1], return_counts=True)
        if 3 in row_count:
        	return True
        elif 3 in col_count:
        	return True
        elif (board[0,0] == player and board[1,1] == player and board[2,2] == player):
        	return True
        elif (board[0,2] == player and board[1,1] == player and board[2,0] == player):
        	return True

        return False
