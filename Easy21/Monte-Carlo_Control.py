from utils import *
from plots import *
import numpy as np
import os
from datetime import datetime


def perform_sequence( N, Q, init_state=None, init_action=None):

    state_sequence = []
    award_sequence = []
    action_sequence = []

    if init_state == None:
        state = initializer()
    else:
        state = init_state

    if init_action != None:
        action = init_action
        action_sequence.append(action)
        state_sequence.append(state)

        print("Performance Sequence: taking action {} in state {}".format(action, state))
        state, award = step(state, action)

        award_sequence.append(award)


    while state != None:
        epsilon = 1
        epsilon = 100 / (100 + np.sum(N[state["dealer_sum"], state["player_sum"], :]))
        action = epsilon_greedy(state, epsilon, Q)
        state_sequence.append(state)
        action_sequence.append(action)

        state, award = step(state, action)

        award_sequence.append(award)

    return state_sequence, award_sequence, action_sequence

def update(state_sequence, award_sequence, action_sequence, N, Q):

    # evaluate the policy 
    for t in range(len(action_sequence)):

        G_t = np.sum(award_sequence)
        dealer_card_value = state_sequence[t]["dealer_sum"]
        player_card_value = state_sequence[t]["player_sum"]
        action = action_sequence[t]

        prevN = N[dealer_card_value, player_card_value, action]
        prevWinCount = Q[dealer_card_value, player_card_value, action] * prevN

        N[dealer_card_value, player_card_value, action] += 1
        Q[dealer_card_value, player_card_value, action] = \
            1 / N[dealer_card_value, player_card_value, action] * \
            (G_t + prevWinCount)

    return N, Q

def monte_carlo_control():
    
    # dealer_first_card, state_sequence, award_sequence, action_sequence, N = initialize_a_sequence()
    # print("begin")
    # print(len(state_sequence))
    # print(len(award_sequence))
    # print(len(action_sequence))
    # print("initialize length")

    Q = np.zeros([11, 22, 2])
    N = np.zeros([11, 22, 2])
    Easy21PathDir = os.path.dirname(os.path.abspath(__file__))
    runDir = "{}/{}".format(Easy21PathDir, datetime.now())
    os.mkdir(runDir)
    stateValuefileNames = []
    policyFileNames = []

    for i in range(10000):

        for dealer_card_value in range(1, 11):
            for player_card_value in range(2, 22):
                for action in [0, 1]:
                    print("=====================Sampling Value: dealer value {}, player value {}, action {} =================="\
                          .format(dealer_card_value, player_card_value, action))
                    state = {"dealer_sum": dealer_card_value,
                             "player_sum": player_card_value}
                    state_sequence, award_sequence, action_sequence = \
                        perform_sequence(N, Q, init_state=state, init_action=action)
                    print("State sequence: {}".format(state_sequence))
                    print("award sequence: {}".format(award_sequence))
                    print("action sequence: {}".format(action_sequence))
                    N, Q = update(state_sequence, award_sequence, action_sequence, N, Q)

        if i % 10 == 0 or i < 10:
            filename = "{}/state-value-function-round-{}.png".format(runDir, i)
            stateValuefileNames.append(filename)
            save_state_value_function(Q, filename)

            filename = "{}/policy-round-{}.png".format(runDir, i)
            policyFileNames.append(filename)
            save_policy(Q, filename)

    gifFileName = "{}/state-value-function-summary".format(runDir)
    create_gif_state_value_function(stateValuefileNames, gifFileName)
    create_gif_state_value_function(policyFileNames, "{}/policy-summary".format(runDir))

    # plot_state_value_function(Q)

    np.save("activation_values", Q)
    np.save("visiting_times", N)

    return Q, N
    

if __name__ == "__main__":
    monte_carlo_control()
