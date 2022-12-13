import sys
import numpy as np


class SimplexSolver:
    eps = 1 / 10 ** 8
    max_iter = 10000
    def __init__(self, source=None, point=None, verbose=False):
        self.verbose = verbose
        if source is not None and point is not None:
            self.n = len(source)
            self.m = len(source[0])
            self.num_arg = self.m - 1

            basis = []
            for i in range(len(point)):
                if point[i] != 0:
                    basis.append(i + 1)

            self.get_first_plan(source, basis)

            if self.verbose:
                print("First plan:")
                self.print_table()

        elif source is not None:
            self.n = len(source)
            self.m = len(source[0])
            self.num_arg = self.m - 1
            opt_func = source[self.n - 1]

            if self.verbose:
                print("Creating table with synthetic basis:")
            self.create_table_with_synthetic_basis(source)

            self.calculate()

            all_null = True
            for j in range(self.m - self.n + 1):
                if self.table[self.n - 1][j] > SimplexSolver.eps:
                    all_null = False
                    break
            if not all_null:
                print(
                    "В результате получения первого опорного плана не все искусственные переменные равны нулю. "
                    "Решений нет!")
                sys.exit()

            new_table = [[0] * (self.m - self.n + 1) for i in range(self.n)]
            for i in range(len(new_table)):
                for j in range(len(new_table[0])):
                    new_table[i][j] = self.table[i][j]

            for j in range(len(new_table[0])):
                sum_col = 0
                for i in range(len(new_table) - 1):
                    sum_col += new_table[i][j] * opt_func[self.basis[i]]
                new_table[len(new_table) - 1][j] = sum_col - opt_func[j]
            new_table[len(new_table) - 1] = list(np.array(new_table[len(new_table) - 1]) * (-1))

            self.table = new_table
            self.n = len(self.table)
            self.m = len(self.table[0])

            if self.verbose:
                print("\nCreated first plan:")
                self.print_table()

    def calculate(self):
        if self.verbose:
            print("First table:")
            self.print_table()
        iteration = 0
        while not self.is_end(iteration):
            iteration += 1
            main_col = self.find_main_col()
            main_row = self.find_main_row(main_col)

            if main_row == -1:
                print("Не удалось выбрать опорный элемент. Задача не имеет решений, так как ОДР не ограничена")
                sys.exit()

            if self.verbose:
                print("Pivot element: (" + str(main_row + 1) + ";" + str(main_col + 1) + ")")

            self.basis[main_row] = main_col

            self.make_step(main_row, main_col)
            if self.verbose:
                self.print_table()

        result = [0 for _ in range(self.num_arg)]
        for i in range(len(self.basis)):
            if self.basis[i] <= self.num_arg:
                result[self.basis[i] - 1] = self.table[i][0]

        return [self.table, result]

    def is_end(self, iteration):
        flag = True
        for j in range(1, self.m):
            if self.table[self.n - 1][j] < -SimplexSolver.eps:
                flag = False
                break
        return flag or iteration >= SimplexSolver.max_iter

    def find_main_col(self):
        main_col = 1
        for j in range(2, self.m):
            if self.table[self.n - 1][j] < self.table[self.n - 1][main_col]:
                main_col = j
        return main_col

    def find_main_row(self, main_col):
        main_row = -1
        for i in range(self.n - 1):
            if self.table[i][main_col] > SimplexSolver.eps:
                main_row = i
                break

        if main_row == -1:
            return -1

        for i in range(main_row + 1, self.n - 1):
            if (self.table[i][main_col] > SimplexSolver.eps) and (
                    self.table[i][0] / self.table[i][main_col] <
                    self.table[main_row][0] / self.table[main_row][main_col]):
                main_row = i

        return main_row

    def make_step(self, main_row, main_col):
        new_table = [[0] * self.m for _ in range(self.n)]

        for j in range(self.m):
            new_table[main_row][j] = self.table[main_row][j] / self.table[main_row][main_col]

        for i in range(self.n):
            if i == main_row:
                continue

            for j in range(self.m):
                new_table[i][j] = self.table[i][j] - (self.table[main_row][j] / self.table[main_row][main_col]) * \
                                  self.table[i][main_col]
                new_table[i][j] = new_table[i][j]

        self.table = new_table

    def get_first_plan(self, source, basis):
        if self.verbose:
            print("Try to get first plan:")
        self.table = source
        self.basis = [-1 for _ in range(len(basis))]

        for basis_arg in basis:
            main_col = basis_arg
            main_row = -1
            for i in range(self.n - 1):
                if self.basis[i] == -1 and self.table[i][main_col] > SimplexSolver.eps:
                    main_row = i

            if main_row == -1:
                print("Невозможно ввести базисные перменные в базис")
                sys.exit()

            if self.verbose:
                print("Pivot element: (" + str(main_row + 1) + ";" + str(main_col + 1) + ")")

            self.basis[main_row] = main_col

            self.make_step(main_row, main_col)
            if self.verbose:
                self.print_table()

    def print_table(self):
        print()
        for i in range(len(self.table)):
            print(self.table[i])
        print()

    def create_table_with_synthetic_basis(self, source):
        self.basis = list()
        self.table = [[0] * (self.m + self.n - 1) for _ in range(self.n)]

        # create first table
        for i in range(self.n):
            for j in range(len(self.table[0])):
                if j < self.m:
                    self.table[i][j] = source[i][j]
                else:
                    self.table[i][j] = 0

            # add basis
            if (self.m + i) < len(self.table[0]):
                self.table[i][self.m + i] = 1
                self.basis.append(self.m + i)

        self.m = len(self.table[0])

        for j in range(self.m):
            sum = 0
            for i in range(self.n - 1):
                sum -= self.table[i][j]
            self.table[self.n - 1][j] = sum
        for basis_col in self.basis:
            self.table[self.n - 1][basis_col] = 0





