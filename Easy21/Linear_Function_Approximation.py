import numpy as np
from utils import *
from plots import *


def feature_mapping(dealer_first_card, player_sum, action):
    feature_vector = np.zeros((3, 6, 2))

    if dealer_first_card in range(1, 5):
        feature_vector[0, :, :] = 1
    if dealer_first_card in range(4, 8):
        feature_vector[1, :, :] = 1
    if dealer_first_card in range(7, 11):
        feature_vector[2, :, :] = 1

    if player_sum in range(1, 7):
        feature_vector[:, 0, :] = 1
    if player_sum in range(4, 10):
        feature_vector[:, 1, :] = 1
    if player_sum in range(7, 13):
        feature_vector[:, 2, :] = 1
    if player_sum in range(10, 16):
        feature_vector[:, 3, :] = 1
    if player_sum in range(13, 19):
        feature_vector[:, 4, :] = 1
    if player_sum in range(16, 22):
        feature_vector[:, 5, :] = 1

    if action == 0:
        feature_vector[:, :, 0] = 1
    if action == 1:
        feature_vector[:, :, 1] = 1

    return feature_vector

def dot(a, b):

    return np.dot(a.flatten(), b.flatten())

def find_max_value_action(dealer_first_card, player_sum, theta):

    feature = feature_mapping(dealer_first_card, player_sum, 1)
    value_1 = dot(feature, theta)

    feature = feature_mapping(dealer_first_card, player_sum, 0)
    value_0 = dot(feature, theta)

    if value_0 > value_1:
        return 0, value_0
    else:
        return 1, value_1


def epsilon_greedy_linear(dealer_first_card, player_sum, theta, epsilon):

    goal = np.random.choice(["random", "greedy"], p=[epsilon, 1 - epsilon])
    value = 0

    if goal == "greedy":

        action, value = find_max_value_action(dealer_first_card, player_sum, theta)

    else:

        action = np.random.choice([0, 1])
        feature = feature_mapping(dealer_first_card, player_sum, action)
        value = dot(feature, theta)

    return action, value


def linear_control():

    gm = 1
    ld = 1
    alpha = 0.01
    epsilon = 0.05

    # store event sequence for off policy learning
    state_sequence = []
    award_sequence = []
    action_sequence = []

    theta = np.random.rand(3, 6, 2)
    E = np.zeros_like(theta)
    cost = np.zeros([11, 22, 2])

    for episode_num in range(1000):

        state = initializer()

        dealer_first_card = state["dealer_sum"]
        action, _ = epsilon_greedy_linear(dealer_first_card, state["player_sum"], theta, epsilon)

        while state != None:
            print("state when starting steps", state)

            feature = feature_mapping(dealer_first_card, state["player_sum"], action)
            next_state, award = step(state, action)

            state_sequence.append(state["player_sum"])
            award_sequence.append(award)
            action_sequence.append(action)

            print(state)
            prev_action = action
            if next_state == None:

                y = award

            else:
                next_action, value = epsilon_greedy_linear(dealer_first_card, next_state["player_sum"], theta, epsilon)

                y = award + gm * value

                action = next_action



            y_hat = dot(feature, theta)
            delta = (y - y_hat)
            E = gm * ld * E + feature
            theta +=  alpha * E * delta
            state = next_state
            cost[dealer_first_card, state["player_sum"], prev_action] = np.square(y - y_hat)

    plot_learning_curve(cost)

if __name__ == '__main__':
    linear_control()