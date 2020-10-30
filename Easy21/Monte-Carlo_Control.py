from utils import *
from plots import *
import numpy as np


def initialize_a_sequence():
    
    state_sequence = []
    award_sequence = []
    action_sequence = []
    state = initializer()
    N = np.zeros([11, 22, 2])
    state_sequence.append(state["player_sum"])
    dealer_first_card = state["dealer_sum"]
    
    while state != None:
        print("state when starting steps", state)
        
        action = 0
        if state["player_sum"] < 17:
            action = 1
        state, award = step(state, action)
        
        if state == None:
            state_sequence.append(state)
            print(state_sequence)
            print("end episode")
        else:
            state_sequence.append(state["player_sum"])
            
            
        
        award_sequence.append(award)
        action_sequence.append(action)
        
        
    return dealer_first_card, state_sequence, award_sequence, action_sequence, N



def perform_sequence( N, Q):
    
    state_sequence = []
    award_sequence = []
    action_sequence = []
    state = initializer()
    state_sequence.append(state["player_sum"])
    dealer_first_card = state["dealer_sum"]
    
    while state != None:
        print("state when starting steps not initializing", state)
        epsilon = 100 / (100 +  np.sum(N[dealer_first_card, state["player_sum"], :]))
        print("epsilon", epsilon, np.sum(N[dealer_first_card, state["player_sum"], :]))
        action = epsilon_greedy(dealer_first_card, state["player_sum"], epsilon, Q)
        state, award = step(state, action)
        print("state when starting steps after one step ", state)
        
        if state == None:
            state_sequence.append(state)
            print(state_sequence)
            print("end episode")
        else:
            state_sequence.append(state["player_sum"])
        award_sequence.append(award)
        action_sequence.append(action)
        
    return dealer_first_card, state_sequence, award_sequence, action_sequence

def update(dealer_first_card, state_sequence, award_sequence, action_sequence, N, Q):
    
    print("state sequence", state_sequence)
    print("award sequence", award_sequence)
    print("action sequence", action_sequence)

    # evaluate the policy 
    for t in range(len(action_sequence)):
        print("Time step")
        print(t)

        G_t = np.sum(award_sequence[t:])
        print("state sequence") 
        print(state_sequence[t])
        print(dealer_first_card)
        print("G_T")
        print(G_t)
        print("N")
        print( N[dealer_first_card, state_sequence[t], action_sequence[t]])
        N[dealer_first_card, state_sequence[t], action_sequence[t]] += 1
        Q[dealer_first_card, state_sequence[t], action_sequence[t]] += 1 / N[dealer_first_card, state_sequence[t], action_sequence[t]] * (G_t - Q[dealer_first_card, state_sequence[t], action_sequence[t]])
        
    return N, Q

def monte_carlo_control():
    
    dealer_first_card, state_sequence, award_sequence, action_sequence, N = initialize_a_sequence()
    print("begin")
    print(len(state_sequence))
    print(len(award_sequence))
    print(len(action_sequence))
    print("initialize length")

    Q = np.zeros([11, 22, 2])

    for i in range(100000):
        
        N, Q = update(dealer_first_card, state_sequence, award_sequence, action_sequence, N, Q)
        dealer_first_card, state_sequence, award_sequence, action_sequence = perform_sequence(N, Q)
        
    plot_state_value_function(Q)

    np.save("activation_values", Q)
    return Q
    

if __name__ == "__main__":
    monte_carlo_control()
