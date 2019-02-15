import random


class safe_player():

    def make_move(self,state,ai_player = 2,human_player = 1):

        board = state.reshape(3,3)

        # Try to win block starts here
        playable_rows = []
        playable_cols = []

        for i in range(3):
            row_count = 0
            col_count = 0
            for j in range(3):

                if board[i,j] == ai_player:
                    row_count+=1

                if board[j,i] == ai_player:
                    col_count+=1


            if row_count == 2:
                playable_rows.append(i)

            if col_count == 2:
                playable_cols.append(i)


        if len(playable_rows) != 0:

            for i in playable_rows:
                for j in range(3):

                    if board[i,j] == 0:
                        return ((i*3)+j)

        if len(playable_cols)!=0:

            for i in range(3):
                for j in playable_cols:

                    if board[i,j] == 0:
                        return ((i*3)+j)


        available_d1 = []
        available_d2 = []

        dig_1_count = 0
        dig_2_count =0
        for i in range(3):
                if board[i,i] == ai_player:
                    dig_1_count+=1
                elif board[i,i] == 0:
                    available_d1.append((i*3)+i)

                if board[i,2-i] == ai_player:
                    dig_2_count+=1
                elif board[i,2-i] == 0:
                    available_d2.append((i*3)+(2-i))

        if dig_1_count == 2 and len(available_d1)!=0:
            return available_d1[0]
        elif dig_2_count == 2 and len(available_d2)!=0 :
            return available_d2[0]



        # Try to win block ends here
        playable_rows = []
        playable_cols = []

        for i in range(3):
            row_count = 0
            col_count = 0
            for j in range(3):

                if board[i,j] == human_player:
                    row_count+=1

                if board[j,i] == human_player:
                    col_count+=1


            if row_count == 2:
                playable_rows.append(i)

            if col_count == 2:
                playable_cols.append(i)

        if len(playable_rows) != 0:

            for i in playable_rows:
                for j in range(3):

                    if board[i,j] == 0:
                        return ((i*3)+j)

        if len(playable_cols)!=0:

            for i in range(3):
                for j in playable_cols:

                    if board[i,j] == 0:
                        return ((i*3)+j)


        available_d1 = []
        available_d2 = []

        dig_1_count = 0
        dig_2_count =0
        for i in range(3):
                if board[i,i] == human_player:
                    dig_1_count+=1
                elif board[i,i] == 0:
                    available_d1.append((i*3)+i)

                if board[i,2-i] == human_player:
                    dig_2_count+=1
                elif board[i,2-i] == 0:
                    available_d2.append((i*3)+(2-i))

        if dig_1_count == 2 and len(available_d1)!=0 :
            return available_d1[0]
        elif dig_2_count == 2 and len(available_d2)!=0:
            return available_d2[0]

        # Try to block code starts here


        # Try to block code ends here

        # Random move
        while True:

            move = random.randint(0,8)

            if state[move] == 0:
                return move
