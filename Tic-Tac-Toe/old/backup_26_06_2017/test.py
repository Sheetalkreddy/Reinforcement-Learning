from Environment import *
from Random_Player import *
from Experince_Buffer import *
from MinMaxPlayer import *




env = Tic_Tac_Toe()

p2 = min_max_player()


done = False
start_state = env.get_state()[0]

state_t = np.copy(start_state)






while  not done:




    ai_move = p2.make_move(state_t)
    state_tm1,reward = env.act(ai_move,2)
    state_tp1,done = state_tm1

    print env.get_state()[0].reshape(3,3)
    if done == True:
        break
    print "AI made move ",ai_move," and reward is",reward

    move = input("Enter between 0-8: ")

    state_tm1,reward = env.act(move,1)
    state_tp1,done = state_tm1

    print "You made move ",move," and reward is",reward


    if done == True:

        print env.get_state()[0].reshape(3,3)

    state_t = np.copy(state_tp1)
