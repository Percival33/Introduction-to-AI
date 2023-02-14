#!/usr/bin/env python3

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from ID3 import ID3
from collections import namedtuple

Dataset = namedtuple('Dataset', 'filepath columns')
import datasets

queue = None


def dfs(node, depth=0):
    global queue
    if queue is None:
        queue = []

    if len(queue) <= depth:
        queue.append([])

    queue[depth].append(str(node))
    if node.nodes is None:
        return

    for next_node in node.nodes:
        dfs(next_node, depth + 1)


def split_data(data: Dataset, train_test_ratio: float = 3 / 2):
    """
        a = train_size, b = test_size
        a/b = train_test_ratio = x
        a = b*x
        a / (a+b) = b*x / (b*x + b) = b*x / b*(x+1) = x / (x+1)
    """

    df = pd.read_csv(data.filepath, names=data.columns)
    x = train_test_ratio
    X_train, X_test, y_train, y_test = \
        train_test_split(df.drop('Class', axis=1), df['Class'], train_size=x / (x + 1), random_state=42)

    return X_train, X_test, y_train, y_test


def plot(predictions, y_test):
    predictions = np.array(predictions)
    y_test = np.array(y_test)
    TP, FN, FP, TN = 0, 0, 0, 0

    values = np.unique(y_test)

    for i, val in enumerate(predictions):
        if y_test[i] == values[0] and predictions[i] == values[0]:
            TP += 1
        elif y_test[i] == values[0] and predictions[i] == values[1]:
            FN += 1
        elif y_test[i] == values[1] and predictions[i] == values[0]:
            FP += 1
        elif y_test[i] == values[1] and predictions[i] == values[1]:
            TN += 1

    print(f'val[0]={values[0]}: {TP+FN}, val[1]={values[1]}: {FP+TN}')
    print(f'{TP:=} {FN:=} \n {FP:=} {TN:=}')
    # print(f'{cnt / len(predictions) * 100:.2f}')
    print(values)

    data = np.array([
        [TP, FN],
        [FP, TN]
    ])
    ax = sns.heatmap(data, annot=True, xticklabels=values, yticklabels=values)
    ax.xaxis.tick_top()
    return ax

def get_percentage(predictions, y_test):
    cnt = 0
    y_test = list(y_test)
    for i, val in enumerate(predictions):
        # print(i, val)
        cnt += 1 if predictions[i] == y_test[i] else 0

    print(f'{cnt / len(predictions) * 100:.2f}')

if __name__ == '__main__':
    dataset = datasets.AL2
    X_train, X_test, y_train, y_test = split_data(dataset)

    id3 = ID3(dataset.columns[1:])
    id3.fit(X_train, y_train)

    predictions = id3.predict(X_test)

    get_percentage(predictions, y_test)
    # plot(predictions, y_test)




    dfs(id3.root)
    for q in queue:
        print(q)
