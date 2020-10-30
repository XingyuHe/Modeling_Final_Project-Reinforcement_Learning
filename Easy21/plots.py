import numpy as np
import matplotlib.pylab as plb
import matplotlib.pyplot as plt

def plot_state_value_function(Q):

    V = np.max(Q, axis=-1)
    fig = plb.figure()
    ax = fig.add_subplot(111, projection='3d')
    x, y = np.meshgrid(range(V.shape[1]), range(V.shape[0]))

    ax.plot_wireframe(x, y, V)
    plb.show()

def plot_learning_curve(cost):
    plt.plot(cost, range(len(cost)))
    plt.show()

def plot_policy(Q):
    optimal_policy = np.argmax(Q, axis=2)
    plt.imshow(optimal_policy)
