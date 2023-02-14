# WSI_22Z

Introduction to Artificial Intelligence - academic course

### Table of contents

- [lab_1.1](#lab_1.1) - Search Space vol. 1
- [lab_1.2](#lab_1.2) - Search Space vol. 2
- [lab_2](#lab_2) - Evolutionary and Genetic Algorithms
- [lab_3](#lab_3) - Deterministic two-player games
- [lab_4](#lab_4) - Regression and Classification
- [lab_5](#lab_5) - Artificial neural networks
- [lab_6](#lab_6) - Reinforcement learning (RL)
- [lab_7](#lab_7) - Bayesian Models

## lab_1.1

_Search Space - Knapsack problem_

**Task:**

Find the optimal solution by exhaustive search. Solve the problem using a heuristic: pack items into a backpack in order of decreasing value-to-weight ratio.

## lab_1.2

_Search Space - Stochastic Gradient Descent_

**Task:**

Please implement the steepest descent/ascent method. We calculate the gradient numerically. Apply the method to find the minimum of the Booth function in 2 dimensions, then to find the minimum of functions 1 to 3 from CEC 2017 in 10 dimensions.

## lab_2

_Evolutionary and Genetic Algorithms - evolutionary algorithm_

**Task:**

Implement a classic evolutionary algorithm without crossover, using tournament selection and elitist succession. The available budget is 10000 evaluations of the objective function. We are optimizing functions number 4 and 5 from CEC 2017 in 10 dimensions. The bounds of the search space are -100 and 100.

## lab_3

_Deterministic two-player games - MiniMax checkers_

**Task:**

Implement the alpha-beta pruning min-max algorithm and apply it to the game of checkers/draughts. Let the evaluation function return the difference between the player's and the opponent's board state.

## lab_4

Regression and Classification - ID3 algorithm

**Task:**

Implement the ID3 classifier (decision tree) with nominal attributes and identity tests. Provide accuracy and confusion matrices for given datasets.

## lab_5

_Artificial neural networks - two-layer perceptron_

**Task:**

Implement a two-layer perceptron and train it to represent the function `J: [-5,5] → R`, given by the formula: `J(x) = sin(xsqrt(5))+cos(xsqrt(3))`.

## lab_6

_Reinforcement learning (RL) - Qlearning agent_

**Task:**
Implement the Q-Learning algorithm and use it to determine a decision policy for the FrozenLake8x8 problem.

In addition to investigating the default reward system (1 for reaching the goal, 0 otherwise), please propose your own system of rewards and penalties, and then compare the results achieved with the default system.

## lab_7

_Bayesian Models - Random data generator using Bayesian network distribution_

**Task:**

Implement a random data generator that follows the distribution represented by a given Bayesian network. The network describes the dependencies between (binary) random variables and is provided as a graph structure and conditional probability tables in a text file. Divide the generated set and use it to train and test the classifier created in previous exercises.

### How to get CEC functions?

```
git clone https://github.com/tilleyd/cec2017-py
cp -R cec2017-py/cec2017 .
```
