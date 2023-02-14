import matplotlib.pyplot as plt
import numpy as np


def create_plot(x: np.array, y: np.array, yh: np.array) -> plt.figure:
    """
        x:  inputs
        y:  outputs
        yh: predicted outputs
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    ax.grid(True)
    plt.plot(x, y, 'r', label='real value')
    plt.plot(x, yh, 'b', label='prediction')
    ax.legend()

    return ax


def plot_loss_func(x: np.array, y: np.array) -> plt.figure:
    """
        x:  inputs
        y:  outputs
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    ax.grid(True)
    plt.plot(x, y, 'r', label='loss function')
    ax.legend()

    return ax
