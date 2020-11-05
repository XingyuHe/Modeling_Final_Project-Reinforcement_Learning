from node import *
import gym
import gym_tictactoe

env = gym.make('TicTacToe-v1', symbols=[-1, 1], board_size=3, win_size=3)
env.reset()
print(env.action_space)
# tree = Monte_Carlo_Tree_Search(env)