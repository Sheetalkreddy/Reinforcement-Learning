from Environment import *
from Random_Player import *
from Experince_Buffer import *
from Agent import *
from Safe_Player import *
from AC import *

env = Tic_Tac_Toe()

p1 = PGAgent(epi=0.7 ,gamma=0.99)
p2 = Random_Player()

memory = Experience_Replay_Buffer(10000)

epcs = 100000
total_wins = 0
total_loses = 0
total_draws = 0
total_invalid = 0

mode = 1
epi = 0.6
for epc in range(epcs):
    epi_reward =[]
    epi_states = []
    epi_actions = []
    env.reset()
    start_state = env.get_state()[0]

    if epc>15000 == 0:
        p2 = safe_player()
    if epc%1000000 == 0:
        if mode == 1:
            mode = 1
        else:
            mode = 1
    if epc%3000 == 0 and epc != 0:
        # p1.setepi(epi)
        epi -= 0.1
        if epi <0.2:
            epi = 0
    if epc>90000:
        epi = 0
    state_t = np.copy(start_state)
    loss = 0
    while True:


        if mode == 1:
            # Player goes_first
            player_move = p1.make_move(state_t)
            state_tm1,reward = env.act(player_move,1)
            epi_reward.append(reward)
            epi_states.append(state_t.reshape(9))
            epi_actions.append(player_move)
            state_tp1,done = state_tm1
            old_state = np.copy(state_t)

            if done == True:
                if reward == 1.0:
                    total_wins+=1
                elif reward == 0.5:
                    total_draws+=1
                elif reward == -1.0:
                    total_loses+=1
                elif reward == -2:
                    total_invalid+=1
                # memory.add (([np.copy(old_state),player_move,reward,np.copy(state_tp1)],done))
                # Save into buffer
                break

            ai_move = p2.make_move(state_tp1)
            state_tm1,reward = env.act(ai_move,2)
            state_tp1,done = state_tm1
            if reward == 0.7:
                total_wins+=1
            elif reward == 0.5:
                total_draws+=1
            elif reward == -0.7:
                total_loses+=1
            elif reward == -1:
                total_invalid+=1
            # Save into buffer
            # memory.add (([np.copy(old_state),player_move,reward,np.copy(state_tp1)],done))

            if done == True:
                break

        else:
            # Player goes second

            ai_move = p2.make_move(state_t)
            state_tm1,reward = env.act(ai_move,2)
            state_tp1,done = state_tm1
            if done == True:
                # Save into buffer
                memory.add (([np.copy(state_t),player_move,reward,np.copy(state_tp1)],done))
                break

            player_move = p1.make_move(state_t)
            state_tm1,reward = env.act(player_move,1)
            print reward
            epi_reward.append(reward)
            epi_states.append(state_t.reshape(9))
            epi_actions.append(player_move)
            state_tp1,done = state_tm1

            # Save into buffer
            # print reward
            # memory.add (([np.copy(state_t),player_move,reward,np.copy(state_tp1)],done))

            if done == True:
                break

        state_t = np.copy(state_tp1)

    # inputs,targets = memory.buffer_get_batch(p1.model,batch_size = 50)

    # print len(epi_reward)
    # print len(epi_states)
    # print len(epi_actions)

    loss += p1.Train(epi_states,epi_actions,epi_reward)[0]

    print "Epoch is ",epc+1,"Loss is",loss,"Total Wins: ",total_wins,"Total Loses:",total_loses,"Total Draws: ",total_draws,"Total Invalids: ",total_invalid
    # break












env.reset()
start_state = env.get_state()[0]
mode = 1#random.randint(1,2)
state_t = np.copy(start_state)
loss = 0

while True:


    if mode == 1:
        # Player goes_first
        player_move = p1.make_move(state_t)
        state_tm1,reward = env.act(player_move,1)
        state_tp1,done = state_tm1
        print "Player move is ",player_move
        if done == True:
            print state_tp1.reshape(3,3)
            # Save into buffer
            break
        print env.get_state()[0].reshape(3,3)

        ai_move = input("Enter your move: ")
        state_tm1,reward = env.act(ai_move,2)
        state_tp1,done = state_tm1

        # Save into buffer
        if done == True:
            print state_tp1.reshape(3,3)

            break

    else:
        # Player goes second
        print env.get_state()[0].reshape(3,3)

        ai_move = input("Enter your move: ")
        state_tm1,reward = env.act(ai_move,2)
        state_tp1,done = state_tm1

        if done == True:
            print state_tp1.reshape(3,3)
            # Save into buffer
            break

        player_move = p1.make_move(state_t)
        state_tm1,reward = env.act(player_move,1)
        state_tp1,done = state_tm1

        # Save into buffer
        if done == True:
            print state_tp1.reshape(3,3)

            break

    state_t = np.copy(state_tp1)
