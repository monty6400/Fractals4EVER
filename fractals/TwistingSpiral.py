from fractals import Fractal
import os


class TwistedSpiral(Fractal):
    max_iterations = 20

    def iter_warning(self):
        return self.iter_num > self.max_iterations

    def get_save_path(self):
        return os.path.join(self.save_path, self.__class__.__name__)

    def functions(self):
        def f1(x, y):
            return 0.5 * x - 0.5 * y, 0.5 * x + 0.5 * y

        def f2(x, y):
            return -0.5 * x - 0.5 * y + 1, -0.5 * x + 0.5 * y

        return [f1, f2]
