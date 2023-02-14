import numpy as np


class FrozenLakeAgent:
    def __init__(
            self,
            map_size: int,
            learning_rate: float,
            epsilon: float,
            discount_factor: float = 0.8,
            n_action: int = 4,
    ):
        np.random.seed(1)
        self.all = 0
        self.cnt = 0
        self.n_action = n_action
        self.q_values = np.zeros((map_size, n_action))
        self.lr = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

        self.training_error = []

    def _act_greedily(self, obs):
        curr_max = np.max(self.q_values[obs])
        tmp = []
        for m in range(self.n_action):
            if self.q_values[obs][m] == curr_max:
                tmp.append(m)

        self.all += 1
        if len(tmp) != self.n_action:
            self.cnt += 1

        return tmp[np.random.randint(low=0, high=len(tmp))]

    def get_action(self, obs: int, testing: bool = False) -> int:
        # return a random action to explore environment (eksploracja)
        if not testing and np.random.uniform() < self.epsilon:
            return np.random.randint(low=0, high=4)

        # with probability (1 - epsilon) act greedily (exploit) (eksploatacja)
        return self._act_greedily(obs)


    def update(
            self,
            obs: int,
            action: int,
            reward: float,
            terminated: bool,
            next_obs: int,
    ):
        # updates the Q-value of an action

        temporal_difference = reward + self.discount_factor * np.max(self.q_values[next_obs]) - self.q_values[obs][
            action]
        self.q_values[obs][action] = (1 - self.lr) * self.q_values[obs][action] + self.lr * (
                reward + self.discount_factor * max(self.q_values[next_obs, :]))
        # self.q_values[obs][action] = self.q_values[obs][action] + self.lr * temporal_difference
        self.training_error.append(temporal_difference)
