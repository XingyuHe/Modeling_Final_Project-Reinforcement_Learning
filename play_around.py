import gym
import highway_env
from pprint import pprint
from matplotlib import pyplot as plt

screen_width, screen_height = 84, 84

config = {
    "observation": {
        "type": "OccupancyGrid",
        "vehicles_count": 15,
        "features": ["presence", "x", "y", "vx", "vy", "cos_h", "sin_h"],
        "features_range": {
            "x": [-100, 100],
            "y": [-100, 100],
            "vx": [-20, 20],
            "vy": [-20, 20]
        },
        "grid_size": [[-27.5, 27.5], [-27.5, 27.5]],
        "grid_step": [5, 5],
        "absolute": False
    }
}
env = gym.make('highway-v0')
env.configure(config)
obs = env.reset()
pprint(obs)

# for _ in range(3):
#     action = env.action_type.actions_indexes["IDLE"]
#     obs, reward, done, info = env.step(action)
#     env.render()

plt.imshow(env.render(mode="rgb_array"))
plt.show()