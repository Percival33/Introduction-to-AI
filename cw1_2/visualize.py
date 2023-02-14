from typing import Any, TypedDict
from venv import create
import numpy as np
import matplotlib.pyplot as plt

class VisualParams(TypedDict):
    max_x: int
    plot_step: float

DEFAULT_VISUAL_PARAMS = {
    'max_x': 100,
    'plot_step': 0.1
}

def draw_contours(func: callable, params: VisualParams):
    # size of plot axes
    x_arr = np.arange(-params['max_x'], params['max_x'], params['plot_step'])
    y_arr = np.arange(-params['max_x'], params['max_x'], params['plot_step'])

    # create 2D grid
    X, Y = np.meshgrid(x_arr, y_arr)
    Z = np.empty(X.shape)

    # count height on plot
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = func(np.array([X[i, j], Y[i, j]]))

    # 20 = Determines the number and positions of the contour lines / regions.
    plt.contour(X, Y, Z, 20)


def draw_arrows(steps: list[np.array], func: callable, arg1: int, arg2: int):

    for i in range(len(steps) - 1):
        dx = steps[i + 1][arg1] - steps[i][arg1]
        dy = steps[i + 1][arg2] - steps[i][arg2]

        plt.arrow(steps[i][arg1], steps[i][arg2], dx, dy, head_width=1, head_length=1, fc='k', ec='k')


def create_plot(x: list[np.array], func: callable, params: VisualParams = DEFAULT_VISUAL_PARAMS, arg1: int = 0, arg2: int = 1):
    draw_contours(func, params)
    
    # arg1, arg2 defines parametrs to draw arrows
    draw_arrows(x, func, arg1, arg2)
    
    plt.show()