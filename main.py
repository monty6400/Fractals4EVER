import fractals
from utils import Visualize


def main():
    initial_points = [[1.0], [1.0]]
    fractal_generator = fractals.BarnsleyFern(initial_points, iter_num=12,
                                               enforce_iter=False, save_path="saved_fractals")
    fractal_generator.iterate()
    visualizer = Visualize(5_000, fractal_generator.points_data)
    visualizer.show()


if __name__ == '__main__':
    main()

"""What is this?
def function1(x, y):
    return x / 3, y / 3


def function2(x, y):
    return x / 3 + 2 / 3, y / 3


def function3(x, y):
    angle = np.pi / 3
    return x / 3 * np.cos(angle) - y / 3 * np.sin(angle) + 1 / 3, x / 3 * np.sin(angle) + y / 3 * np.cos(angle)


def function4(x, y):
    angle = 5 * np.pi / 3
    return x / 3 * np.cos(angle) - y / 3 * np.sin(angle) + 1 / 2, x / 3 * np.sin(angle) + y / 3 * np.cos(
        angle) - 1 / 3 * np.sin(angle)
"""
