import numpy as np
from SimplexSolver import SimplexSolver

class LinearProgrammingTask:
    def __init__(self, f, restrictions, start_point, verbose=False):
        self.func_coef = list(f)
        self.verbose = verbose

        for i in range(len(f) - 1, 0, -1):
            f[i], f[i - 1] = f[i - 1], f[i]

        table = [[0] * (len(restrictions[0]) - 1) for _ in range(len(restrictions) + 1)]
        table[len(restrictions)] = list(f)
        for i in range(len(restrictions)):
            for j in range(len(restrictions[0])):
                if j < len(restrictions[0]) - 2:
                    table[i][j + 1] = restrictions[i][j]
                elif j == len(restrictions[0]) - 2:
                    table[i][0] = restrictions[i][j + 1]

        # change '>=' to '<='
        for i in range(len(restrictions)):
            if restrictions[i][len(restrictions[0]) - 2] == ">=":
                table[i] = list(np.array(table[i]) * (-1))

        # change '<=' to '='
        for i in range(len(restrictions)):
            if restrictions[i][len(restrictions[0]) - 2] != "=":
                restrictions = np.array(restrictions)
                table = np.array(table)
                new_column = np.zeros(len(restrictions) + 1)
                new_column[i] = 1
                table = np.column_stack((table, new_column))

        for i in range(len(table)):
            if table[i][0] < 0:
                table[i] = list(np.array(table[i]) * (-1))

        self.table = table
        self.f = f
        self.start_point = start_point

    def solve(self):
        if self.start_point is None:
            simplex = SimplexSolver(source=self.table)
            result_table, result = simplex.calculate()
        else:
            simplex = SimplexSolver(source=self.table, point=self.start_point)
            result_table, result = simplex.calculate()
        end_result = []
        result_f = 0

        for i in range(len(self.func_coef) - 1):
            end_result.append(round(result[i], 4))
            result_f += self.func_coef[i] * end_result[i]

        print("___________")
        print("RESULT:")
        print(end_result)
        print("f= " + str(result_f))