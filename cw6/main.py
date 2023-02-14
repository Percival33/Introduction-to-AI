from abc import ABC, abstractmethod
import gymnasium as gym
import numpy as np
from tqdm import tqdm
from FrozenLakeAgent import FrozenLakeAgent
from test_cases import tests
import matplotlib.pyplot as plt

SIDE = 8
MAP_SIZE = SIDE ** 2
N_EPISODES = 10_000
ACTION_LIMIT = 200  # per episode
REWARD_MIN, REWARD_MAX = -1, 10


def my_reward(obs: int, action: int, next_obs: int, done: bool):
    if done and next_obs == MAP_SIZE - 1:
        return REWARD_MAX
    if done and next_obs != MAP_SIZE - 1:
        return REWARD_MIN
    if obs == next_obs:
        return -0.1
    return 0


def training(env, agent, default: bool = True) -> float:
    wynik, played_episodes = 0, 0
    for episode in tqdm(range(N_EPISODES)):
        played_episodes += 1
        obs, info = env.reset()
        done = False

        for _ in range(ACTION_LIMIT):
            if done:
                break

            action = agent.get_action(obs)
            next_obs, reward, terminated, truncated, info = env.step(action)

            if next_obs == MAP_SIZE - 1:
                wynik += 1

            if not default:
                reward = my_reward(obs, action, next_obs, terminated)

            agent.update(obs, action, reward, terminated, next_obs)

            done = terminated or truncated
            obs = next_obs

    # print(f'{wynik}/{played_episodes} = {round(wynik / played_episodes, 3)}')
    return round(wynik / played_episodes, 3)


def testing(env, agent) -> float:
    wynik, played_episodes = 0, 0
    for episode in tqdm(range(N_EPISODES // 10)):
        played_episodes += 1
        obs, info = env.reset()
        done = False

        for _ in range(ACTION_LIMIT):
            if done:
                break

            action = agent.get_action(obs, testing=True)
            next_obs, reward, terminated, truncated, info = env.step(action)

            if next_obs == MAP_SIZE - 1:
                wynik += 1

            done = terminated or truncated
            obs = next_obs

    return round(wynik / played_episodes, 3)
    # return f'{wynik}/{played_episodes} = {round(wynik / played_episodes, 3)}'


def stats(agent):
    print(f'len training error: {len(agent.training_error)}')

    print(f'\t\tL\tD\tR\tU')
    for pos in range(agent.q_values.shape[0]):
        print(f'POS={pos}\t', end='')
        for d in range(agent.q_values.shape[1]):
            print(round(agent.q_values[pos][d], 3), end='\t\t')
        print()
        # if (pos + 1) % 4 == 0:
        #     print()


def create_plot(env, agent):
    rolling_length = 1000
    fig, axs = plt.subplots(ncols=2, figsize=(12, 5))
    axs[0].set_title("Episode rewards")
    reward_moving_average = (
            np.convolve(
                np.array(env.return_queue).flatten(), np.ones(rolling_length), mode="valid"
            )
            / rolling_length
    )
    axs[0].plot(range(len(reward_moving_average)), reward_moving_average)
    axs[1].set_title("Episode lengths")
    length_moving_average = (
            np.convolve(
                np.array(env.length_queue).flatten(), np.ones(rolling_length), mode="same"
            )
            / rolling_length
    )
    axs[1].plot(range(len(length_moving_average)), length_moving_average)
    plt.tight_layout()
    plt.show()


def main(learning_rate: float = 0.9, epsilon: float = 0.1, discount_factor: float = 0.8, default: bool = True,
         plot: bool = False) -> float:
    env = gym.make("FrozenLake-v1", is_slippery=False, desc=None, map_name="8x8")

    if plot:
        env = gym.wrappers.RecordEpisodeStatistics(env, deque_size=N_EPISODES)

    agent = FrozenLakeAgent(
        map_size=MAP_SIZE,
        learning_rate=learning_rate,
        epsilon=epsilon,
        discount_factor=discount_factor
    )

    test_res = None

    if default:
        train_res = training(env, agent, default=True)
        test_res = testing(env, agent)
        # stats(agent)
    else:
        train_res = training(env, agent, default=False)
        test_res = testing(env, agent)
        stats(agent)

    if plot:
        create_plot(env, agent)

    # stats(agent)
    return test_res
    # return f'default:{default}\ttrain: {train_res}\ttest: {test_res}\ngreedily cnt: {agent.cnt}/{agent.all} = {agent.cnt / agent.all}'


def get_stats(arr):
    if arr is None:
        return
    arr = np.array(arr)
    return f'{arr.min():.3}\t{arr.mean():.3}\t{arr.max():.3}\t{arr.std():.3}'


if __name__ == '__main__':
    # hyperparameters
    # learning_rate = 0.9
    # epsilon = 0.1
    # discount_factor = 0.8

    default = []
    custom = []

    for id, test in enumerate(tests):
        print(id)
        for case in test:
            default.append(
                main(learning_rate=case['lr'], epsilon=case['epsilon'], discount_factor=case['discount_factor'],
                     default=True, plot=True)
            )

        print()

    # print(f'default: {get_stats(default)}')
    print(f'default: {default}')

    for id, test in enumerate(tests):
        print(id)
        for case in test:
            custom.append(
                main(learning_rate=case['lr'], epsilon=case['epsilon'], discount_factor=case['discount_factor'],
                     default=False, plot=True)
            )

        print()

    # print(f'custom: {get_stats(custom)}')
    print(f'custom: {custom}')
