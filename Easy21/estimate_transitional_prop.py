import numpy as np
import copy
# from utils import *

def draw_randomly(initialize=False):
        sample_space = list(range(1, 11))
        sample_space.extend([10, 10])
        random_number = np.random.choice(sample_space)
        return random_number

transitional_prop = np.zeros([11, 22, 11, 22])
def find_transitional_prob():
    N = 100000
    transitional_counter = np.zeros([11, 22, 11, 22])
    for dealer_card_value in range(1, len(transitional_prop)):
        for player_card_value in range(2, len(transitional_prop[dealer_card_value])):

            # print(sum(transitional_prop[dealer_card_value, player_card_value, dealer_card_value,:]))

            for _ in range(N):
                card = draw_randomly()
                new_card_value = player_card_value + card
                if new_card_value < 22:
                    transitional_counter[dealer_card_value, player_card_value, dealer_card_value, new_card_value] += 1
    for dealer_card_value in range(1, len(transitional_prop)):
        for player_card_value in range(2, len(transitional_prop[dealer_card_value])):
            for new_card_value in range(2, len(transitional_prop[dealer_card_value])):
                transitional_prop[dealer_card_value, player_card_value, dealer_card_value, new_card_value] \
                    = transitional_counter[dealer_card_value, player_card_value, dealer_card_value, new_card_value] / N


def if_terminal(state):

    dealer_card = state[0]
    player_card = state[1]

    if player_card > 21:
        return True
    return False

dealer_only_winning_probability = np.ones([11, 22])
def MC_prob_winning_dealer_only(state):

    if dealer_only_winning_probability[state[0], state[1]] != 1:
        return  dealer_only_winning_probability[state[0], state[1]]

    if state[1] > 21:
        dealer_only_winning_probability[state[0], state[1]]  = 0

    numTrials = 100000
    ans = 0.0
    for i in range(numTrials):

        trial_state = copy.deepcopy(state)
        while trial_state[0] < 17:
            trial_state[0] += draw_randomly()

        if trial_state[0] < trial_state[1]:
            ans += 1
        if trial_state[0] > 21:
            ans += 1

    print(state, ans / numTrials)
    dealer_only_winning_probability[state[0], state[1]] = ans/numTrials
    return ans/numTrials


winning_probability = np.ones([11, 22, 2])
def find_winning_probability(state, action):

    if winning_probability[state[0], state[1], action] != 1:
        return winning_probability[state[0], state[1], action]
    if if_terminal(state) == True:
        # Monte Carlo the probability of winning given the state
        return MC_prob_winning_dealer_only(state)
    ans = 0
    if action == 1:
        transitional_prop_state = transitional_prop[state[0], state[1], state[0], :]
        for new_card_value in range(state[1] + 1, len(transitional_prop_state)):
            new_state = [state[0], new_card_value]
            R_new_state_1 = find_winning_probability(new_state, 1)
            R_new_state_0 = find_winning_probability(new_state, 0)
            ans += transitional_prop_state[new_card_value] * max(R_new_state_1, R_new_state_0)

    if action == 0:
        ans = MC_prob_winning_dealer_only(state)

    winning_probability[state[0], state[1], action] = ans

    return ans


find_transitional_prob()
# Calculate the winning probabilities of all possibe state action pair
for dealer_card_value in range(1, 11):
    for player_card_value in range(2, 22):
        for action in range(2):
            find_winning_probability([dealer_card_value, player_card_value], action)
np.save("winning_probability", winning_probability)


# Find out which state action pair did not iterate through
for dealer_card_value in range(11):
    for player_card_value in range(22):
        for action in range(2):
            if winning_probability[dealer_card_value, player_card_value, action] == 1:
                print(dealer_card_value, player_card_value, action)

