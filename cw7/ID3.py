import numpy as np
import pandas as pd

from Solver import Solver
from Node import Node


class ID3(Solver):
    def __init__(self, feature_names: list[str]):
        self.root = None
        self.feature_names = np.array(feature_names, dtype='U')

    def get_parameters(self):
        return {}

    @staticmethod
    def _entropy(U: np.array):
        if len(U) == 0:
            return 0

        U = U[:, 0]  # 0 column is a class
        classes = np.unique(U)
        freq = [list(U).count(cl) / len(U) for cl in classes]

        return -1 * sum(cl_freq * np.log(cl_freq) for cl_freq in freq)

    def _inf(self, d: int, U: list[any]):
        s = 0
        for val in np.unique([X[d] for X in U]):
            subset = np.array([X for X in U if X[d] == val])  # U_j
            if len(subset) == 0:
                continue
            s += len(subset) / len(U) * self._entropy(subset)

        return s

    def _inf_gain(self, d: int, U: np.array):
        return self._entropy(U) - self._inf(d, U)

    def _get_max_inf_gain(self, U):
        if U.shape[1] == 1:
            return None

        return np.argmax([self._inf_gain(d, U) for d in range(1, U.shape[1])])

    def _build_tree(self, X, y, node, feature_names):
        if node is None:
            node = Node()

        unique, counts = np.unique(y, return_counts=True)
        node.pred = y[np.argmax(counts), 0]

        if len(unique) == 1:
            # node is a leaf 1 case
            assert node.pred == y[0, 0]
            # node.pred = y[0, 0]
            return node

        if X.shape[1] == 0:  # no more attributes to split on
            # node is a leaf - class with most occurrences
            assert node.pred == y[np.argmax(counts), 0]

            return node

        d = self._get_max_inf_gain(
            np.concatenate((np.reshape(y, (-1, 1)), X), axis=1)
        )

        attr_values = np.unique([x for x in X[:, d]])

        node.attr = d
        node.feature = feature_names[d]
        node.nodes = []

        for val in attr_values:
            bad_rows = [r for r in range(X.shape[0]) if X[r, d] != val]

            new_X = np.delete(X, np.s_[d], 1)  # delete columns
            new_X = np.delete(new_X, bad_rows, 0)  # delete bad rows
            new_y = np.reshape(np.delete(y, bad_rows, 0), (-1, 1))  # delete bad rows

            child = self._build_tree(new_X, new_y, Node(val), np.delete(feature_names, np.s_[d]))
            node.nodes.append(child)

        return node

    def fit(self, X: pd.DataFrame, y: pd.DataFrame):
        X, y = np.array(X), np.array(y)
        y = np.reshape(y, (-1, 1))
        self.root = self._build_tree(X, y, self.root, self.feature_names)

    def _get_prediction(self, node, X):
        if X.shape[0] == 1 or node.nodes is None:
            return node.pred

        for next_node in node.nodes:
            if str(next_node.edge) == X[node.attr]:
                return self._get_prediction(next_node, np.delete(X, np.s_[node.attr]))

        return node.pred

    def predict(self, X: pd.DataFrame):
        X = np.reshape(np.array(X), (-1, len(self.feature_names)))

        return [self._get_prediction(self.root, X[i]) for i in range(X.shape[0])]
