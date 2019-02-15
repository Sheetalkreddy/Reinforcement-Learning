from Safe_Player import *
from Random_Player import *
from Environment import *
from numpy import array, array_equal, allclose
import os
os.environ['KERAS_BACKEND']='theano'

from keras.models import model_from_json, Model
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.recurrent import LSTM

p1 = safe_player()

p2 = Random_Player()

Memory = []

epochs = 10

env = Tic_Tac_Toe()

StateHistory =[]
ActionHistory =[]

for ep in range(epochs):

    env.reset()
    gameover = False
    EpiMem = []
    EpiOuts =[]
    while not gameover:
        st = env.get_state()[0]


        p1Move = p1.make_move(st,ai_player = 1,human_player = 2)

        count = len(EpiMem)
        if count == 0:
            EpiMem.append([np.copy(st)])
            EpiOuts.append(p1Move)
        else:
            old = list(EpiMem[count-1])
            old.append(np.copy(st))
            EpiMem.append(old)
            EpiOuts.append(p1Move)

        stp1,reward= env.act(p1Move)
        stp1,gameover = stp1
        if gameover:
            print env.get_state()[0].reshape(3,3)
            break
        p2Move = p2.make_move(stp1)
        stp1,reward= env.act(p2Move,mode =2 )
        stp1,gameover = stp1

        if gameover:
            print env.get_state()[0].reshape(3,3)

    StateHistory.append(list(EpiMem))
    ActionHistory.append(list(EpiOuts))

UseHistory = 5
NbActions = 0

def getIndex(myarr,list_arrays):
    for i in range(len(list_arrays)):
        if np.array_equal(myarr,list_arrays[i]):
            return i
def arreq_in_list(myarr, list_arrays):
    return next((True for elem in list_arrays if array_equal(elem, myarr)), False)

Inputs =  []
Inter_Outs = []
for i in StateHistory:
    for j in i:
        indi_in = np.zeros((UseHistory,9))

        for k in range(min(5,len(j))):
            indi_in[k] = j[len(j)-1-k].reshape(1,9)

        Inputs.append(np.copy(indi_in))
        state_index = [np.array_equal(i,x) for x in StateHistory].index(True)
        Inter_Outs.append(ActionHistory[state_index][i.index(j)])


Final_Inputs= []

Final_Targets = []


for i in range(len(Inputs)):

    if not arreq_in_list(Inputs[i], Final_Inputs):
        Final_Inputs.append(Inputs[i])
        Final_Targets.append(np.copy(np.zeros((1,9))))
        Final_Targets[len(Final_Targets)-1][0][Inter_Outs[i]] += 1
    else:
        index = getIndex(Inputs[i],Final_Inputs)
        Final_Targets[index][0][Inter_Outs[i]] += 1

for i in range(len(Final_Targets)):
    Final_Targets[i] = Final_Targets[i]/np.sum(Final_Targets[i][0])

Final_Inputs = np.array(Final_Inputs)
Final_Targets = np.array(Final_Targets)
print Final_Inputs.shape
print Final_Targets.shape
model = Sequential()
model.add(LSTM(Final_Targets.shape[2],input_shape=(Final_Inputs.shape[1],Final_Inputs.shape[2]), return_sequences=False))
model.compile(optimizer='adam',loss='categorical_crossentropy')
model.fit(Final_Inputs,Final_Targets.reshape(Final_Targets.shape[0],Final_Targets.shape[2]),validation_split = 0.2,verbose = 1,batch_size = 1)
