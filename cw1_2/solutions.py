# Marcin Jarczewski
# WSI lab1_2

from typing import Any, TypedDict
from venv import create
from cec2017.functions import f1, f2, f3
from autograd import grad
import numpy as np
import matplotlib.pyplot as plt
from visualize import create_plot

class Params(TypedDict):
    upper_bound: float
    dimensionality: int
    beta: float
    repetitions: int
    iterations: int

def gradient_descent(func: callable, params: Params) -> list[Any]:
    results = []
    
    for num in range(params['repetitions']):
        curr_rep = []
        
        # random starting point
        x = np.random.uniform(-params['upper_bound'], params['upper_bound'], size=params['dimensionality'])
        
        for _ in range(params['iterations']):
            curr_rep.append(x)
            d = grad(func)(x)
            x = x - params['beta'] * d

        results.append(curr_rep)

    return results

def booth(x: np.array) -> np.array:
    return (x[0] + 2 * x[1] - 7) ** 2 + (2 * x[0] + x[1] - 5) ** 2

def print_results(results: list[Any]):
    print(f'parameters: {results["params"]}')
    
    for repet in range(len(results['steps'])):
        print(f'REPETITION: {repet}')
    
        for id, val in enumerate(results['steps'][repet]):
            print(f'\titer: {id} x: {val}')

        if repet + 1 < len(results):
            print('\n\n')

if __name__ == '__main__':
    params = {
        'upper_bound': 100,
        'dimensionality': 10,
        'beta': 1e-18,
        'repetitions': 1,
        'iterations': 1000
    }

    func = f2

    results = {
        'params': params,
        'steps': gradient_descent(func, params)
    }

    print(results['steps'][0][-1], func(results['steps'][0][-1]))
    create_plot(results['steps'][0], func, {'max_x': 150, 'plot_step': 0.1}, 0, 1)
