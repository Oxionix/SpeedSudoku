import Solver
import random
import copy
from time import time_ns


class Feld:
    def __init__(self, matrix, base):   # normal 9x9 has base 3
        self.matrix = matrix
        self.isSud = None      # ist eindeutig lösbar?
        self.base = base
        if base < 2:
            raise Exception("Base not smaller than 2")
        # self.solve()

    def solve(self):
        self.isSud = Solver.Solver.issolve(self)

    def solutions(self):
        pass

    def count_empty(self):
        s = 0
        for i in self.matrix:
            s += i.count(0)
        return s

    def getmatrix(self):
        return copy.deepcopy(self.matrix)

    def getbase(self):
        return self.base

    def isSolveable(self):
        if self.isSud is None:
            self.solve()
        return self.isSud

    def __repr__(self):
        return "Sudoku"

    def strv2(self):
        ret = ""
        for i in self.matrix:
            for j in i:
                ret += str(j) + " "
            ret = ret[:-1]
            ret += ";"
        ret = ret[:-1]
        return ret

    def print_as_list(self):
        print(self.matrix)

    def __str__(self):
        ret = ""
        for i in self.matrix:
            for j in i:
                ret += str(j) + " "
            ret += "\n"
        """for count2, i in enumerate(self.matrix):
            for count1, j in enumerate(i):
                ret += str(j)
                if count1 % self.base == self.base - 1:
                    ret += "|"
                else:
                    ret += " "
            ret += "\n"
            if count2 % self.base == self.base - 1:
                for x in range(self.base*self.base):
                    ret += "--"
                ret += "\n"
        """
        return ret

    def check(self, positions, b):
        m = self.getmatrix()
        for pos in positions:
            m[pos[0]][pos[1]] = 0
        f = Feld(m, self.base)
        if b:
            t1 = time_ns()
            temp = f.isSolveable()
            t2 = time_ns()
            t = (t2 - t1) / 1000000000
            # print(t)
            if t > 2:
                # f.print_as_list()
                # print(f)
                pass
            return f.isSolveable()
        else:
            return f

    @staticmethod
    def make_sud(base):
        empty = [[0 for x in range(base**2)] for y in range(base**2)]
        f = Feld(empty, base)
        g = Solver.Solver.solve(f)
        pfad = [(x, y) for x in range(base**2) for y in range(base**2)]
        random.shuffle(pfad)
        r = base**4
        l = 0
        m = 0
        while l < r-1:
            m = int((r+l)/2)

            if g.check(pfad[:m], True):
                l = m
            else:
                r = m
        return g.check(pfad[:m], False)

    @staticmethod
    def make_sudtest(base):
        empty = [[0 for x in range(base ** 2)] for y in range(base ** 2)]
        f = Feld(empty, base)
        g = Solver.Solver.solve(f)
        pfad = [(x, y) for x in range(base ** 2) for y in range(base ** 2)]
        random.shuffle(pfad)
        r = base ** 4
        l = 0
        m = 0
        while l < r - 1:
            m = int((r + l) / 2)

            if g.checktest(pfad[:m], True):
                l = m
            else:
                r = m
        return g.checktest(pfad[:m], False)

    def checktest(self, positions, b):
        m = self.getmatrix()
        for pos in positions:
            m[pos[0]][pos[1]] = 0
        f = Feld(m, self.base)
        if b:
            t1 = time_ns()
            temp = f.isSolveabletest()
            t2 = time_ns()
            t = (t2 - t1) / 1000000000
            print(t)
            if t > 2:
                f.print_as_list()
                print(f)
            return f.isSolveabletest()
        else:
            return f

    def isSolveabletest(self):
        if self.isSud is None:
            self.solvetest()
        return self.isSud

    def solvetest(self):
        print(1)
        t1 = time_ns()
        self.isSud = Solver.Solver.istest(self)
        t2 = time_ns()
        print((t2-t1)/1000000000)
        print(2)
        t3 = time_ns()
        self.isSud = Solver.Solver.issolve(self)
        t4 = time_ns()
        print((t4-t3)/1000000000)

