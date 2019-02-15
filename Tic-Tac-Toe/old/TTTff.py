import os
os.environ['KERAS_BACKEND'] = 'theano'
import numpy as np
import random
import keras
from keras.models import Sequential
from keras.layers.core import Dense


class TTT:
	def __init__(self):
		self.board = np.zeros((3,3))
		self.done = False
		self.user = 1
		self.ai_user = 2
		self.user_chance = 1

	def reset(self):
		self.board = np.zeros((3,3))
		self.done = False

	def change_user_chance(self):
		if self.user_chance == 1:
			self.user_chance = 2
		else:
			self.user_chance = 1

	def check_block(self,player,move):

		if player == self.ai_user:
			return False

		row = move/3
		col = move%3
		cnt_row = 0
		cnt_col = 0
		for i in range(3):
			if self.board[row,i] == self.ai_user:
				cnt_row+=1

			if self.board[i,col] == self.ai_user:
				cnt_col += 1

		if cnt_col == 2 or cnt_row == 2:
			return True

		cnt_diag1 = 0
		cnt_diag2 = 0

		if row == col:
			for i in range(3):
				if self.board[i,i] == self.ai_user:
					cnt_diag1 += 1
		if ((row == 1 and col == 1) or (row == 0 and col == 2) or (row == 2 and col == 0)):
			for i in range(3):
				if self.board[i,2-i] == self.ai_user:
					cnt_diag2 += 1

		if cnt_diag1 == 2 or cnt_diag2 == 2:
			return True

		return False



	def check_win(self,player,move):
		ar = np.where(self.board == player)
		u, row_count = np.unique(ar[0], return_counts=True)
		u, col_count = np.unique(ar[1], return_counts=True)
		if 3 in row_count:
			self.done = True
			return 1
		elif 3 in col_count:
			self.done = True
			return 1
		elif (self.board[0,0] == player and self.board[1,1] == player and self.board[2,2] == player):
			self.done = True
			return 1
		elif (self.board[0,2] == player and self.board[1,1] == player and self.board[2,0] == player):
			self.done = True
			return 1

		elif np.count_nonzero(self.board)==9:
			self.done = True
			return 0
		else:
			self.done = False
			return 0

	def get_state(self):
		return (self.board.reshape(9,),self.done)
		# Return state is (board,done)
	def make_move(self,move,player):
		row = move/3
		col = move%3

		if self.board[row,col] == 0:
			self.board[row,col] = player

			if self.check_win(player,move) == 1:
				return (self.get_state(),0.7)
			elif self.check_win(player,move) == 0 and self.done == True:
				return (self.get_state(),0.3)
			elif self.check_win(player,move) == 0:
				return (self.get_state(),0.0)

		else:
			self.done = True
			return (self.get_state(),-0.9)

	def random_ai(self,ai_player):

		while True:
			move = np.random.randint(0,9)
			row = move/3
			col = move%3
			if self.board[row,col] == 0:
				self.board[row,col] = ai_player

				if self.check_win(ai_player,move) == 1:
					return (self.get_state(),-0.7)
				elif self.check_win(ai_player,move) == 0 and self.done == True:
					return (self.get_state(),0.3)
				elif self.check_win(ai_player,move) == 0:
					return (self.get_state(),0.0)
					# return value is (state,reward)
				break

	def ai_act(self,ai_mode):
		if ai_mode == 1:
			ret_2 = self.random_ai(self.ai_user)
		elif ai_mode == 2:
			ret_2 = self.safe_ai()
		return ret_2

	def act(self,move,ai_mode = 1):

		if self.user_chance == 1:
			ret_1 = self.make_move(move,self.user)
			return ret_1

		elif self.user_chance == 2:
			ret_2 = self.make_move(move,self.user)
			return ret_2

	def safe_ai(self):
		while True:
			move = self.safe_ai_move(self.ai_user,self.user)
			row = move/3
			col = move%3

			if self.board[row,col] == 0:
				self.board[row,col] = self.ai_user

				if self.check_win(self.ai_user,move) == 1:
					return (self.get_state(),-0.7)
				elif self.check_win(self.ai_user,move) == 0 and self.done == True:
					return (self.get_state(),0.3)
				elif self.check_win(self.ai_user,move) == 0:
					return (self.get_state(),0.0)
					# return value is (state,reward)
				break

	def safe_ai_move(self,ai_player,human_player):
        # Try to win block starts here
		board = self.board.reshape(3,3)
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
			row = move/3
			col = move%3
			if board[row,col] == 0:
				return move

	def player_act(self,move):
		if self.user_chance == 1:
			ret_1 = self.make_move(move,self.user)
			print self.board.reshape(3,3)
			if self.done == True:
				return ret_1
			ret_2 = self.make_move(input("Please enter your move :"),self.ai_user)
			return ret_2

		if self.user_chance == 2:
			ret_1 = self.make_move(input("Please enter your move :"),self.ai_user)
			if self.done == True:
				return ret_1
			ret_2 = self.make_move(move,self.user)
			return ret_2


class Replay_Buffer():
	def __init__(self,max_size):
		self.buff= []
		self.max_size = max_size

	def add_mem(self,memory):
		self.buff.append(memory)
		if len(self.buff) > self.max_size:
			del self.buff[0]

	def get_batch(self,batch_size,model,discount = 0.4):
		if batch_size > len(self.buff):
			batch_size = len(self.buff)
		count = 0
		pop = random.sample(range(0,len(self.buff)),batch_size)

		inputs = np.zeros(( batch_size, 9))
		targets = np.zeros((inputs.shape[0], 9))
		for i in pop:
			# Memory of the form ((state_t,action,reward,state_t+1),done)
			state_t = self.buff[i][0][0]
			state_tp1 = self.buff[i][0][3]
			reward = self.buff[i][0][2]
			action = self.buff[i][0][1]
			done = self.buff[i][1]

			inputs[count] = state_t


			indi_target = model.predict(state_t.reshape(1,9),batch_size =1 ).reshape(1,9)
			targets[count] = indi_target
			Q_sa = np.max(model.predict(state_tp1.reshape(1,9),batch_size =1 ).reshape(1,9)[0])
			if done == True:
				targets[count,action] = reward
			else:
				targets[count,action] = reward + discount * Q_sa

			count+=1

		return np.array(inputs),np.array(targets)


# model used for the training
model = Sequential()
model.add(Dense(100,input_dim=9,activation = 'relu'))
model.add(Dense(200,activation = 'relu'))
model.add(Dense(9))
model.compile(loss = 'mse',optimizer = 'adam')
model.summary()


env = TTT()
mem = Replay_Buffer(10000)
epc = 1
epi = 1.0# Exploration vs Exploitation

epi_decay = 0.1
nb_actions = 9
batch_size = 100
win_count = 0
wins = 0
losses = 0
draws = 0
invalids = 0


ai_mode =1 # 1 for random ai # 2 for safe ai

for ep in range(epc):

	env.reset()


	loss = 0.
	game_over = False
	input_t = env.get_state()[0].reshape(1,9)
	loss = 0

	if ep%2000 == 0 and ep != 0 :
		epi = epi - epi_decay

	if ep%5000 == 0 and ep != 0 :
		if ai_mode == 1:
			ai_mode = 2
		else:
			ai_mode = 1

	if ep%30000000 == 0 and ep!=0 :
		env.change_user_chance()


	while game_over == False:

		input_ = np.copy(input_t)

		if env.user_chance ==2 and game_over!= False:

			state_tp1,reward = env.ai_act(ai_mode)
			game_over = state_tp1[1]
			input_ = np.copy(state_tp1[0]).reshape(1,9)

		if game_over == False:
			if np.random.rand() <= epi:
				action = np.random.randint(0, nb_actions, size=1)[0]
			else:
				q = model.predict(input_,batch_size = 1)
				action = np.argmax(q[0])

			state_tp1,reward = env.act(action,ai_mode)
			game_over = state_tp1[1]

		if env.user_chance == 1 and game_over == False:
				state_tp1,reward = env.ai_act(ai_mode)

		if reward == 0.7:
			wins+=1
		if reward == -0.9:
			invalids+=1
		if reward == 0.3:
			draws+=1
		if reward == -0.7:
			losses+=1

		input_t1 = state_tp1[0].reshape(1,9)
		game_over = state_tp1[1]

		mem.add_mem(((input_,action,reward,np.copy(input_t1)),game_over))
		input_t = input_t1

	inputs,targets = mem.get_batch(batch_size,model)



	loss+=model.train_on_batch(inputs,targets)

	print "Epoch Number: ",ep,"Loss is ",loss,"Total Wins: ",wins,"Total Losses: ",losses,"Total Draws: ",draws,"Invalids: ",invalids


test_cases = 1
test_win =0
test_lose = 0
test_draw = 0
test_invalid = 0
for i in range(test_cases):
	env.reset()
	game_over = False

	input_t = env.get_state()[0]

	while game_over == False:

		input_ = np.copy(input_t).reshape(1,9)

		if env.user_chance ==2 :
			state_tp1,reward = env.ai_act(ai_mode)
			game_over = state_tp1[1]
			input_ = np.copy(state_tp1[0]).reshape(1,9)

		if game_over == False:


			if np.random.rand() <= epi:
				action = np.random.randint(0, nb_actions, size=1)[0]
			else:
				q = model.predict(input_,batch_size = 1)
				action = np.argmax(q[0])

			state_tp1,reward = env.act(action,ai_mode)

		if env.user_chance == 1:
				state_tp1,reward = env.ai_act(ai_mode)

		if reward == 0.7:
			test_win+=1
		if reward == -0.9:
			test_invalid+=1
		if reward == 0.3:
			test_draw+=1
		if reward == -0.7:
			test_lose+=1

		input_t1 = state_tp1[0].reshape(1,9)
		game_over = state_tp1[1]


		input_t = input_t1

print "Number of Wins: ",test_win,"Number of Draws: ",test_draw,"Number of Losses: ",test_lose,"Number of Invalids: ",test_invalid
