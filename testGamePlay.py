from gameState import *
import gym_TicTacToe
import gym
import copy


env = gym.make('TTT-v4')
obs = env.reset()
obs = np.reshape(obs, [3,3])
game = GameState(action=None, env=env, obs=obs, reward=None, done=False, info=None)

# assert str(game) == ("000000000")

assert game.legal_moves == [(0, 0), (0, 1), (0, 2),
                              (1, 0), (1, 1), (1, 2),
                              (2, 0), (2, 1), (2, 2)]

# 0pening game
game.step_row_col(1, 1)  # 1
game.step_row_col(0, 2)  # 0
game.step_row_col(1, 2)  # 1
game.step_row_col(1, 0)  # 0
game.step_row_col(2, 1)  # 1

assert str(game) == ("~~2\n"
                     "211\n"
                     "~1~\n")

# Keep track of the current game state so we can some alternate end
# games from this point later
game_copy1 = copy.deepcopy(game)
game_copy2 = copy.deepcopy(game)

# End game #1
game.step_row_col(0, 0)  # 0
game.step_row_col(0, 1)  # 1 plays a winning horizontal line

assert game.winner() == '1'

# End game #2
game_copy1.step_row_col(0, 0)  # 0
game_copy1.step_row_col(2, 2)  # 1
game_copy1.step_row_col(2, 0)  # 0 plays a winning vertical line

assert game_copy1.winner() == '2'
assert not game_copy1.legal_moves

# End game #3
game_copy2.step_row_col(2, 2)  # 0
game_copy2.step_row_col(0, 0)  # 1
game_copy2.step_row_col(0, 1)  # 0
game_copy2.step_row_col(2, 0)  # 1
assert game_copy2.winner() == 'Tie'
assert str(game_copy2) == ("122\n"
                           "211\n"
                           "112\n")

