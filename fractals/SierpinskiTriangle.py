from fractals import Fractal
import os


class SierpinskiTriangle(Fractal):
    max_iterations = 11

    def iter_warning(self):
        return self.iter_num > self.max_iterations

    def get_save_path(self):
        return os.path.join(self.save_path, self.__class__.__name__)

    def functions(self):
        def f1(x, y):
            return x / 2, y / 2

        def f2(x, y):
            return x / 2, y / 2 + 1 / 2

        def f3(x, y):
            return x / 2 + 1 / 2, y / 2

        return [f1, f2, f3]
