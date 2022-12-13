import numpy as np
import scipy.linalg as linalg

from MarkovChains.Plotter import Plotter


class MarkovChain:
    condition_matrix = \
        [
            [0.1, 0.2, 0.3, 0.1, 0.2, 0.1, 0, 0],
            [0.2, 0.4, 0, 0, 0, 0.2, 0.2, 0],
            [0.05, 0.05, 0.45, 0.31, 0.04, 0.05, 0.05, 0],
            [0.25, 0.05, 0.15, 0.05, 0.05, 0.05, 0.15, 0.25],
            [0.01, 0.01, 0.05, 0.33, 0.15, 0.05, 0.2, 0.2],
            [0.14, 0.05, 0.01, 0.3, 0.14, 0.05, 0.01, 0.3],
            [0.2, 0.1, 0.05, 0.05, 0.2, 0.1, 0.05, 0.25],
            [0.05, 0.05, 0.45, 0.31, 0.04, 0.05, 0, 0.05],
        ]

    def __init__(self, eps=1e-6, initial_state_row=2, max_steps=1000):
        self.__validate_matrix()
        self.condition_matrix = np.array(self.condition_matrix)

        self.eps = eps
        self.initial_state_row = initial_state_row
        self.max_steps = max_steps

        self.plotter = None

    def solve_numerically(self):
        previous_vector = self.condition_matrix[self.initial_state_row]
        current_vector = previous_vector @ self.condition_matrix

        spent_steps = 0
        deviations = []

        while abs(np.std(previous_vector - current_vector) >= self.eps) and spent_steps <= self.max_steps:
            previous_vector = current_vector
            current_vector = current_vector @ self.condition_matrix

            deviations.append(np.std(current_vector))
            spent_steps += 1

        self.plotter = Plotter(np.linspace(0, spent_steps, spent_steps), deviations)
        return current_vector

    def solve_analytically(self):
        eigenvalues, left_eigenvectors = linalg.eig(self.condition_matrix, right=False, left=True)
        vector = left_eigenvectors[:, 0]
        vector_norm = [x / np.sum(vector).real for x in vector]
        return vector_norm

    def plot_results(self):
        self.plotter.plot()

    def __validate_matrix(self):
        eps = 1e-10
        for row in self.condition_matrix:
            if abs(sum(row) - 1) > eps:
                raise Exception("Probabilities matrix is incorrect")


chain = MarkovChain()
print(chain.solve_numerically())
print(chain.solve_analytically())
chain.plot_results()
