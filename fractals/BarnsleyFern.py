from fractals import Fractal


class BarnsleyFern(Fractal):
    max_iterations = 11

    def functions(self):
        def f1(x, y):
            return x*0, 0.16*y

        def f2(x, y):
            return 0.85*x + 0.04*y, -0.04*x + 0.85*y + 1.6

        def f3(x, y):
            return 0.2*x - 0.26*y, 0.23*x + 0.22*y + 1.6

        def f4(x, y):
            return -0.15*x + 0.28*y, 0.26*x + 0.24*y + 0.44

        return [f1, f2, f3, f4]
