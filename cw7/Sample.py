#!/usr/bin/env python3
from typing import Any

import numpy as np
import json


class Sample:
    def __init__(self, filename: str = 'graph.json', number: int = 100):
        self.filename = filename
        self.net = None
        self.number = number

    def get_previous_decisions(self, prev_nodes: list[str], sample: dict[Any]) -> int:
        crr = 0
        for prev_name in prev_nodes:
            crr <<= 1
            # crr |= sample[prev_name]
            crr |= 1 if sample[prev_name] == "T" else 0
        return crr

    def _get_sample(self):
        if self.net is None:
            with open(self.filename, 'r') as f:
                self.net = json.load(f)

        sample = {}

        for name in self.net:
            node = self.net[name]

            if not node['in']:
                prob = node['1']
            else:
                choice = self.get_previous_decisions(node['in'], sample)
                prob = node['1'][choice]

            tmp = np.random.random()
            if tmp < prob:
                sample[name] = "T"
            else:
                sample[name] = "F"
            # print(name, tmp, sample[name])

        return list(sample.values())

    def get_samples(self):
        results = []
        for _ in range(self.number):
            results.append(self._get_sample())

        return results

    def get_names(self):
        if self.net is None:
            with open(self.filename, 'r') as f:
                self.net = json.load(f)

        return list(self.net.keys())

    def save_samples(self, filename: str = 'examples.json'):
        samples = self.get_samples()
        names = self.get_names()
        data = {
            "names": names,
            "samples": samples
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        with open('abc.data', 'w') as f:
            for x in samples:
                print(f'{x[0]},{x[1]},{x[2]},{x[3]}', file=f)
