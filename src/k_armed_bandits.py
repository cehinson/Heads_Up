import numpy as np
from numba import njit
import pandas as pd
import matplotlib.pyplot as plt


@njit()
def k_armed_bandits_simulation(
    seed,
    k=10,
    epsilon=0.0,
    steps=1_000,
    runs=2_000,
):

    actions = np.array([x for x in range(0, k)])
    # true reward values for each action
    np.random.seed(seed)
    true_values = np.array([np.random.normal() for _ in range(0, k)])
    # compute average rewards per run
    result = np.zeros((steps))

    for _ in range(runs):
        Q = np.zeros((len(actions)))
        N = np.zeros((len(actions)))
        for t in range(steps):
            # epsilon greedy action selection
            A = np.argmax(Q)
            if np.random.rand() < epsilon:
                A = np.random.choice(actions)
            # get reward from environment
            R = np.random.normal(loc=true_values[A])
            # update Q
            N[A] += 1
            Q[A] = Q[A] + 1/N[A] * (R - Q[A])
            # keep track of rewards
            result[t] += (R * 1/float(runs))

    return result


if __name__ == "__main__":

    results = []
    epsilons = [0.0, 0.01, 0.05, 0.1]
    for e in epsilons:
        results.append(k_armed_bandits_simulation(42, epsilon=e, steps=1_000, runs=3_000))

    stats = pd.DataFrame(results)
    stats = stats.transpose()
    stats.columns = epsilons
    stats.plot(kind='line')
    plt.show()
