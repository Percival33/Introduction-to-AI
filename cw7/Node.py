class Node:
    def __init__(self, edge=None, pred=None, attr=None, feature=None, nodes=None):
        self.edge = edge  # edge value
        self.pred = pred  # predicted class
        self.attr = attr  # column id
        self.feature = feature  # feature name
        self.nodes = nodes  # list of children nodes

    def __str__(self):
        return f"predict: {self.pred}  edge: {self.edge} feature: {self.feature} attr: {self.attr}"

    def __repr__(self):
        return f'val: {self.pred}\tattr: {self.attr}\tnodes: {self.nodes}'