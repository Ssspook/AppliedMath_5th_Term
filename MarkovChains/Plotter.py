import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, x_values, y_values):
        self.x_values = x_values
        self.y_values = y_values

    def plot(self):
        plt.plot(self.x_values, self.y_values)
        plt.show()