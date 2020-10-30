import numpy as np
import copy


def epsilon_greedy(dealer_first_card, player_sum, epsilon, Q):
        goal = np.random.choice(['random', 'optimal'], p=[epsilon, 1 - epsilon])

        if goal == 'random':
                action = np.random.randint(0, 2)
                print("action in e greedy", goal, action)
        else:
                Q_s = Q[dealer_first_card, player_sum, :]

                action = np.argmax(Q_s)
                print(
                "decide to be greedy", action, "player sum", player_sum, "state currntly in", Q_s, "action to take",
                action)
        return action


def draw_randomly(initialize=False):
        sample_space = list(range(1, 11))
        sample_space.extend([10, 10])
        random_number = np.random.choice(sample_space)
        return random_number


def initializer():
        player_card = draw_randomly(True)
        dealer_card = draw_randomly(True)
        
        state = {"dealer_sum" : dealer_card, 
                 "player_sum" : player_card}

        return state



def step(state, action):
        print("take you to the next step")
        next_state = state
	
        if action == 1:
                player_card = draw_randomly()
                next_state["player_sum"] += player_card
                print(player_card)
                if next_state["player_sum"] > 21:
                        print("busted")
                        return None, -1
                else:
                        return next_state, 0

        if action == 0:
                print("action step", action)

                if next_state['dealer_sum'] > 21:
                        return None, 1

                if next_state["dealer_sum"] < 17:
                        dealer_card = draw_randomly()
                        print(dealer_card)
                        next_state["dealer_sum"] += dealer_card
                        print("state when recur for dealer", next_state)
                        step(next_state, 0)

                if next_state["dealer_sum"] > next_state["player_sum"]:
                        return None, -1
                
                if next_state["dealer_sum"] < next_state["player_sum"]:
                        return None, 1
                
                if next_state["dealer_sum"] == next_state["player_sum"]:
                        return None, 0


