import numpy as np
import os
import matplotlib.pylab as plb
import matplotlib.pyplot as plt
import imageio
from mpl_toolkits.mplot3d import Axes3D

def create_gif_state_value_function(sourceFileNames, targetFileName):
    images = []
    for filename in sourceFileNames:
        images.append(imageio.imread(filename))
    imageio.mimsave('{}.gif'.format(targetFileName), images)

def save_state_value_function(Q, filename):

    V = np.max(Q, axis=-1)
    fig = plb.figure()
    ax = fig.add_subplot(projection='3d')
    x, y = np.meshgrid(range(V.shape[1]), range(V.shape[0]))

    ax.plot_surface(x, y, V, rstride=1, cstride=1,
                cmap='viridis',linewidths=0.2)
    # ax.contour3D(x, y, V, 50, cmap='binary')
    # ax.plot_wireframe(x, y, V, color="black")
    ax.view_init(elev=44, azim=-140)
    plt.ylabel("Dealer Card Value")
    plt.xlabel("Player Card Value")
    title = filename[filename.find("round"):]
    plt.title(title)
    plt.savefig(filename)
    plt.close()

def plot_state_value_function(Q):

    V = np.max(Q, axis=-1)
    fig = plb.figure()
    ax = fig.add_subplot(projection='3d')
    x, y = np.meshgrid(range(V.shape[1]), range(V.shape[0]))

    ax.plot_surface(x, y, V, rstride=1, cstride=1,
                cmap='viridis',linewidths=0.2)
    # ax.contour3D(x, y, V, 50, cmap='binary')
    # ax.plot_wireframe(x, y, V, color="black")
    ax.view_init(elev=44, azim=-140)
    plb.show()

def plot_learning_curve(cost):
    plt.plot(cost, range(len(cost)))
    plt.show()

def plot_policy(Q):
    optimal_policy = np.argmax(Q, axis=2)
    plt.imshow(optimal_policy)

def save_policy(Q, fileName):
    optimal_policy = np.argmax(Q, axis=2)
    title = fileName[fileName.find("round"):]
    plt.title("MDP Policy")
    plt.imshow(optimal_policy)
    plt.savefig(fileName)
    plt.close()



# q = np.load("/Users/xhe/Desktop/Modeling_Final_Project-Reinforcement_Learning/Easy21/activation_values.npy")
# # save_state_value_function(q)
# plot_state_value_function(q)
# plot_policy(q)
# # #
# for dealer_card_value in range(11):
#     for player_card_value in range(22):
#         for action in range(2):
#             if q2[dealer_card_value, player_card_value, action] == 1:
#                 q2[dealer_card_value, player_card_value, action] = 0
# np.save("winning_probability", q2)
# #
# # n = np.load("/Users/xhe/Desktop/Modeling_Final_Project-Reinforcement_Learning/Easy21/visiting_times.npy")
q2 = np.load("/Users/xhe/Desktop/Modeling_Final_Project-Reinforcement_Learning/winning_probability.npy")
plot_policy(q2)
save_policy(q2, "./MDPPolicy.png")
save_state_value_function(q2, "./MDPMaxR.png")
# plot_state_value_function(q2)

run_dir = os.path.dirname(os.path.abspath(__file__))
print(run_dir)




