#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 16:51:50 2021

@author: Rafał Biedrzycki
Kodu tego mogą używać moi studenci na ćwiczeniach z przedmiotu Wstęp do Sztucznej Inteligencji.
Kod ten powstał aby przyspieszyć i ułatwić pracę studentów, aby mogli skupić się na algorytmach sztucznej inteligencji. 
Kod nie jest wzorem dobrej jakości programowania w Pythonie, nie jest również wzorem programowania obiektowego, może zawierać błędy.

Nie ma obowiązku używania tego kodu.
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from DlNet import DlNet
import ploting
import config
from test_cases import tests


def q(x: np.array):
    return np.sin(x * np.sqrt(config.P[0] + 1)) + np.cos(x * np.sqrt(config.P[1] + 1))


def create_title(neurons: int, iters: int, l_rate: int, batch_size: int):
    return f"neurons:{neurons}, iterations:{iters}, learning rate:{l_rate}, batch size:{batch_size}"


def save_plot(X: np.array, Y: np.array, yh, title: str):
    ax = ploting.create_plot(X, Y, yh)
    plt.title(title)
    # plt.show()

    ext = 'png'
    filename = 'img/' + title + '.' + ext

    plt.savefig(filename, format=ext)
    # plt.show()
    plt.close()
    print(f'Saved new image: {filename}')


def save_loss_plot(values, title: str):
    x = [val[0] for val in values]
    y = [val[1] for val in values]

    ax = ploting.plot_loss_func(x, y)
    plt.title(title)

    ext = 'png'
    filename = 'img/loss func for: ' + title + '.' + ext

    plt.savefig(filename, format=ext)
    # plt.show()
    plt.close()
    print(f'Saved new image: {filename}')


def main(neurons: int = 20, iters: int = 2000, l_rate: int = 0.1, batch_size: int = 100):
    X = np.linspace(config.L_BOUND, config.U_BOUND, config.SIZE)
    Y = q(X)

    np.random.seed(1)

    nn = DlNet(l_rate, batch_size, neurons)
    nn.train(X, Y, iters)

    yh = []
    loss = 0

    for x in np.linspace(config.L_BOUND, config.U_BOUND, config.SIZE):
        y_tmp = nn.predict(x)
        loss += nn.nloss(q(x), y_tmp)
        yh.append(nn.predict(x))

    title = create_title(neurons, iters, l_rate, batch_size)

    save_plot(X, Y, yh, title)
    save_loss_plot(nn.loss_func_values(), title)
    return f'loss: {loss}, MSE: {loss / config.SIZE}'


if __name__ == '__main__':
    tests_size = sum(len(test) for test in tests)
    test_id = 1

    results = []

    for test in tests:
        for case in test:
            print(f'{test_id} / {tests_size}')
            loss_str = main(neurons=case['neurons'], iters=case['iters'], l_rate=case['l_rate'],
                            batch_size=case['batch_size'])

            results.append(f'{test_id} / {tests_size}: {loss_str}')
            test_id += 1

    ''' with open('img/results.json', "w") as f:
        json.dump(results, f, indent=4) '''

