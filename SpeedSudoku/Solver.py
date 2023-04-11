import Feld
import random
from time import time_ns


class Solver:
    def __init__(self, f):
        self.f = f

    @staticmethod
    def gen_sol(f, max_time):
        def putNumber(x, y, num, arr, base):
            size = base * base
            for i in range(0, size):
                if arr[x][i] == num:
                    return False
            for i in range(0, size):
                if arr[i][y] == num:
                    return False
            for i in range(0, base):
                for j in range(0, base):
                    if arr[(x // base) * base + i][(y // base) * base + j] == num:
                        return False
            return True

        def solve_gen(matrix, base, t0, max_time):     # 2d-arr as input
            # print(matrix)
            t1 = time_ns()
            if (t1 - t0)/1000000000 > max_time:
                raise TimeoutError
            size = base*base
            for i in range(0, size):
                for j in range(0, size):
                    if matrix[i][j] == 0:
                        temp = list(range(1, size+1))
                        random.shuffle(temp)
                        for num in temp:
                            if putNumber(i, j, num, matrix, base):
                                matrix[i][j] = num
                                yield from solve_gen(matrix, base, t0, max_time)
                                matrix[i][j] = 0
                        return
            yield Feld.Feld(matrix, base)

        matrix = f.getmatrix()
        base = f.getbase()
        t1 = time_ns()
        s = solve_gen(matrix, base, t1, max_time)
        yield from s

    @staticmethod
    def test(f, max_time):
        def putNumber(x, y, num, arr, base):
            size = base * base
            for i in range(0, size):
                if arr[x][i] == num:
                    return False
            for i in range(0, size):
                if arr[i][y] == num:
                    return False
            for i in range(0, base):
                for j in range(0, base):
                    if arr[(x // base) * base + i][(y // base) * base + j] == num:
                        return False
            return True

        def solve_gen(matrix, base, t0, max_time, path):  # 2d-arr as input
            # print(matrix)
            t1 = time_ns()
            if (t1 - t0) / 1000000000 > max_time:
                raise TimeoutError
            size = base * base
            for i, j in path:
                if matrix[i][j] == 0:
                    temp = list(range(1, size + 1))
                    random.shuffle(temp)
                    for num in temp:
                        if putNumber(i, j, num, matrix, base):
                            matrix[i][j] = num
                            yield from solve_gen(matrix, base, t0, max_time, path)
                            matrix[i][j] = 0
                    return
            yield Feld.Feld(matrix, base)

        def make_path(f):
            base = f.getbase()
            l = base**2
            m = f.getmatrix()
            reihen = [set() for x in range(l)]
            spalten = [set() for x in range(l)]
            felder = [set() for x in range(l)]
            for x in range(l):
                for y in range(l):
                    if not m[y][x]:
                        continue
                    else:
                        reihen[y].add(m[y][x])
                        spalten[x].add(m[y][x])
                        felder[(y//3) * 3 + x//3].add(m[y][x])

            d = {}
            for x in range(l):
                for y in range(l):
                    d[(y, x)] = len(reihen[y] | spalten[x] | felder[(y//3) * 3 + x//3])
            s = sorted(d.items(), key=lambda x:x[1], reverse=True)

            return [x[0] for x in s]

        p = make_path(f)
        matrix = f.getmatrix()
        base = f.getbase()
        t1 = time_ns()
        s = solve_gen(matrix, base, t1, max_time, p)
        yield from s

    @staticmethod
    def issolve(f):
        def foo(f):    # returns wether is solveable
            g = Solver.gen_sol(f, 2)
            sol = next(g)
            if next(g, None) is None:
                return True
            else:
                return False

        try:
            return foo(f)
        except TimeoutError:
            return False

    @staticmethod
    def istest(f):
        def foo(f):  # returns wether is solveable
            g = Solver.test(f, 2)
            sol = next(g)
            if next(g, None) is None:
                return True
            else:
                return False

        try:
            return foo(f)
        except TimeoutError:
            return False

    @staticmethod
    def solve(f):
        g = Solver.gen_sol(f, 10)
        try:
            return next(g)
        except TimeoutError:
            return Solver.solve(f)
