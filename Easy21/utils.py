import numpy as np
import copy


def epsilon_greedy(state, epsilon, Q):
        dealer_card_value = state["dealer_sum"]
        player_card_value = state["player_sum"]
        goal = np.random.choice(['random', 'optimal'], p=[epsilon, 1 - epsilon])

        if goal == 'random':
                action = np.random.randint(0, 2)
        else:
                Q_s = Q[dealer_card_value, player_card_value, :]
                action = np.argmax(Q_s)
        print("Epsilon greedy: taking actions according to {} policy. The action is {}. \
        The state action value function is {}".format(goal, action, Q[dealer_card_value, player_card_value, :]))
        return action


def draw_randomly(initialize=False):
        sample_space = list(range(1, 11))
        sample_space.extend([10, 10])
        random_number = np.random.choice(sample_space)
        return random_number


def initializer():
        player_card = draw_randomly() + draw_randomly()
        dealer_card = draw_randomly()
        
        state = {"dealer_sum" : dealer_card, 
                 "player_sum" : player_card}

        return state


def step(state, action):
        next_state = copy.deepcopy(state)
	
        if action == 1:
                player_card = draw_randomly()
                next_state["player_sum"] += player_card
                print("PLAYER drawing card of value {}, reaching state {}".format(player_card, next_state))
                if next_state["player_sum"] > 21:
                        return None, 0
                else:
                        return next_state, 0

        if action == 0:

                while next_state["dealer_sum"] < 17:
                        dealer_card = draw_randomly()
                        next_state["dealer_sum"] += dealer_card
                        print("dealer drawing card of value {}, reaching state {}".format(dealer_card, next_state))

                if next_state['dealer_sum'] > 21:
                        return None, 1

                elif next_state["dealer_sum"] > next_state["player_sum"]:
                        return None, 0
                
                elif next_state["dealer_sum"] < next_state["player_sum"]:
                        return None, 1
                
                elif next_state["dealer_sum"] == next_state["player_sum"]:
                        return None, 0


