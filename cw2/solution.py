#!/usr/bin/env python
# Marcin Jarczewski
# WSI cw 2 2022

from collections import namedtuple
from typing import NamedTuple, TypedDict
from cec2017.functions import f4, f5
import numpy as np
import time
import json

best_spec = namedtuple("BestSpeciman", ['point', 'quality'])


class Params(TypedDict):
    dimensionality: int
    upper_bound: float
    budget: int
    mu: int
    sigma: float
    elite: int


def create_population(params: Params) -> np.array:
    population = np.empty(shape=(params.get('mu'), params.get('dimensionality')))

    for i in range(params.get('mu')):
        population[i] = np.random.uniform(
            -params.get('upper_bound'), params.get('upper_bound'),
            size=params.get('dimensionality')
        )

    return population


def print_list(x: np.array) -> None:
    for id, val in enumerate(x):
        print(f"{id}: {val}")


def reproducate(population: np.array, quality: list[float]) -> np.array:
    mu = len(population)

    a = np.random.randint(mu, size=mu)
    b = np.random.randint(mu, size=mu)

    # print("q: ", quality)
    # print("a: ", a)
    # print("b: ", b)

    new_population = np.where(quality[a] > quality[b], b, a)  # goal is to minimalize function
    # print(new_population)  
    return np.array([population[i] for i in new_population])


def mutate(population: np.array, params: Params) -> np.array:
    gaussian = np.random.normal(0, params.get('sigma'), params.get('dimensionality'))

    population = np.array(population, dtype=np.float64)
    population += gaussian

    return population


def succesion(population: np.array, mutants: np.array,
              quality: list[float], mutants_quality: list[float],
              params: Params) -> tuple[np.array, list[float]]:
    kth_best_id = np.argsort(quality)[:params.get('elite')]

    new_population = np.empty(shape=(params.get('elite'), params.get('dimensionality')))
    for id, val in enumerate(kth_best_id):
        new_population[id] = population[val]

    new_quality = np.empty(shape=(params.get('elite')))
    for id, val in enumerate(kth_best_id):
        new_quality[id] = quality[val]

    new_population = np.concatenate((new_population, mutants))
    new_quality = np.concatenate((new_quality, mutants_quality))

    kth_worst_id = np.argsort(new_quality)[-params.get('elite'):]
    for id in kth_worst_id:
        new_quality[id] = np.inf

    new_population = np.delete(new_population, np.isinf(new_quality), axis=0)
    new_quality = np.delete(new_quality, np.isinf(new_quality))

    # print("np: ", new_population.shape, "nq: ", new_quality.shape)
    # print("pop: ", population.shape, "mut: ", mutants.shape)

    # print(new_population)
    # print(new_quality)

    return new_population, new_quality


def run_ea(func: callable, params: Params) -> NamedTuple:
    population = create_population(params)

    # ocena
    quality = np.array([func(i) for i in population])

    # print_list(population)
    # print_list(quality)

    # znajdz najlepszego
    best_specimen = best_spec(population[quality.argmin()], quality.min())
    # assert func(best_specimen.point) == best_specimen.quality

    iterations = params.get('budget') // params.get('mu')
    print(f'iterations: {iterations}')

    # petla
    for t in range(iterations):
        # reprodukcja
        reproduction = reproducate(population, quality)

        # operacje genetyczne (krzyzowanie/mutacja)
        mutants = mutate(reproduction, params)

        # ocena
        mutants_quality = np.array([func(i) for i in mutants])

        # znajdz najlepszego
        best_mutant = best_spec(mutants[mutants_quality.argmin()], mutants_quality.min())

        # aktualizacja najlepszego
        if best_mutant.quality < best_specimen.quality:
            best_specimen = best_mutant

        # sukcesja
        population, quality = succesion(population, mutants, quality, mutants_quality, params)

    # print_list(population)
    return best_specimen


def save_results(results: list[best_spec], params: Params):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    with open(f'results/{timestr}-qual.json', 'w') as f:
        json.dump({
            'params': params,
            'points': [res.quality for res in results]
        }, f, indent=2)

        # print(params,"\n", file=f)
        # for res in results:
        #     print(res.quality, '\n', file=f)

    with open(f'results/{timestr}-all.txt', 'w') as f:
        print(params, "\n", file=f)
        for res in results:
            print(res.quality, '\t', res.point, '\n', file=f)


if __name__ == '__main__':
    params = {
        'dimensionality': 10,
        'upper_bound': 100,
        'budget': 10_000,
        'mu': 55,  # size of population
        'sigma': 2,  # strength of mutation
        'elite': 1  # size of elite
    }

    TRIES = 50
    FUNC = f5

    results = np.empty(shape=TRIES, dtype=object)
    for i in range(TRIES):
        print("no: ", i)
        results[i] = run_ea(FUNC, params)

    # print(results)

    q = np.array([res.quality for res in results])
    print(f'min\t\tśr\t\tstd\t\tmax')
    ans = f'{q.min():.3f}\t\t{q.mean():.3f}\t\t{q.std():.3f}\t\t{q.max():.3f}'
    print(ans.replace('.', ','))

    save_results(results, params)
