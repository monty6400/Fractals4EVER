import math

import torch

from fractals import Fractal


class TwistedSpiral(Fractal):
    max_iterations = 20

    def functions(self):
        def f1(x, y):
            return math.cos(50) * x + math.sin(50) * y, -math.sin(50) * x + math.cos(50) * y

        def f2(x, y):
            return 0.5 * x, 0.5 * y

        def f3(x, y):
            return 0.3 * x, 0.7 * y

        def f4(x, y):
            return torch.sin(y), 0.76 * x

        return [f1, f2, f3, f4]
