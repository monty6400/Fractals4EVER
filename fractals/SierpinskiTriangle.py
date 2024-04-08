from fractals import Fractal


class SierpinskiTriangle(Fractal):
    max_iterations = 11

    def functions(self):
        def f1(x, y):
            return x / 2, y / 2

        def f2(x, y):
            return x / 2, y / 2 + 1 / 2

        def f3(x, y):
            return x / 2 + 1 / 2, y / 2

        return [f1, f2, f3]
