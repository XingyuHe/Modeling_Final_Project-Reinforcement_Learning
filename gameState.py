import gym_TicTacToe
import gym
import numpy as np
from copy import deepcopy

class GameState(object):

    def __init__(self, action, step_info, env):
        self.env = env
        self.obs, self.reward, self.done, self.info = step_info
        self.action = action
        self.done = False
        self.legal_moves = self.generate_legal_moves()

    def action_space(self):
        return range(self.env.n_actions)

    def reset(self):
        self.env.reset()

    def generate_legal_moves(self):
        """
        Returns a list of the legal actions from the current state,
        where an action is the placement of a marker 'X' or 'O' on a board
        position, represented as a (row, col) tuple, for example:
          [(2, 1), (0, 0)]
        would indicate that the positions (2, 1) and (0, 0) are available to
        place a marker on. If the game is in a terminal state, returns an
        empty list.
        """
        if self.done:
            return []

        possible_moves = set()
        for row in range(3):
            for col in range(3):
                if self.obs[row][col] == 0:
                    possible_moves.add(row * 3 + col)

        return possible_moves

    def step(self, action):

        next_env = deepcopy(self.env)
        obs, done, reward, info = next_env.step(action)

        child_gameState = GameState(action, [obs, done, reward, info], next_env)

        return child_gameState

    def turn(self):
        """
        Returns the player whose turn it is: 1 or 2
        """
        num_1 = 0
        num_2 = 2
        for row in range(3):
            for col in range(3):
                if self.obs[row][col] == 1:
                    num_1 += 1
                elif self.obs[row][col] == 2:
                    num_2 += 1
        if num_1 == num_2:
            return 1
        else:
            return 2

    def winner(self):

        if self.done == False:
            return None

        for player in [1, 0]:
            # Check for winning horizontal lines
            for row in range(3):
                accum = 0
                for col in range(3):
                    if self.obs[row][col] == player:
                        accum += 1
                if accum == 3:
                    return player

            # Check for winning vertical lines
            for col in range(3):
                accum = 0
                for row in range(3):
                    if self.obs[row][col] == player:
                        accum += 1
                if accum == 3:
                    return player

            # Check for winning diagonal lines (there are 2 possibilities)
            option1 = [self.obs[0][0],
                       self.obs[1][1],
                       self.obs[2][2]]
            option2 = [self.obs[2][0],
                       self.obs[1][1],
                       self.obs[0][2]]
            if all(marker == player for marker in option1) \
                    or all(marker == player for marker in option2):
                return player

            # Check for ties, defined as a board arrangement in which there are no
            # open board positions left and there are no winners (note that the
            # tie is not being detected ahead of time, as could potentially be
            # done)
        accum = 0
        for row in range(3):
            for col in range(3):
                if self.obs[row][col] == ' ':
                    accum += 1
        if accum == 0:
            return 'Tie'

        return None

    def __str__(self):
        return str(self.obs)