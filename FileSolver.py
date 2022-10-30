import json

from LinerProgrammingTask import LinearProgrammingTask


class FileSolver:
    def __init__(self, path):
        file = open(path)
        self.data = json.load(file)

    def solve_all(self, verbose=False):
        for i, task in enumerate(self.data):
            print("Solving number " + str(i + 1))
            f, constraints, start_point = task["f"], task["constraints"], task["start_point"]
            LinearProgrammingTask(
                f=f,
                restrictions=constraints,
                start_point=start_point,
                verbose=verbose
            ).solve()
            print()

    def solve_specific(self, number, verbose=False):
        task = self.data[number - 1]
        f, constraints, start_point = task["f"], task["constraints"], task["start_point"]
        LinearProgrammingTask(
            f=f,
            restrictions=constraints,
            start_point=start_point,
            verbose=verbose
        ).solve()
