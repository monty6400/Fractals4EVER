from fractals import Fractal


class TwistedSpiral(Fractal):
    max_iterations = 20

    def functions(self):
        def f1(x, y):
            return 0.5 * x - 0.5 * y, 0.5 * x + 0.5 * y

        def f2(x, y):
            return -0.5 * x - 0.5 * y + 1, -0.5 * x + 0.5 * y

        return [f1, f2]
