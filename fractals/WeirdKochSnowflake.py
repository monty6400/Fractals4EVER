from fractals import Fractal
import torch


class WeirdKochSnowflake(Fractal):
    max_iterations = 9

    def functions(self):
        def f1(x, y):
            return x / 3, y / 3

        def f2(x, y):
            return x / 3 + 2 / 3, y / 3

        def f3(x, y):
            angle = torch.tensor(torch.pi / 3).to(self.device)
            return x / 3 * torch.cos(angle) - y / 3 * torch.sin(angle) + 1 / 3, x / 3 * torch.sin(angle) + y / 3 * torch.cos(angle)

        def f4(x, y):
            angle = torch.tensor(2 * torch.pi / 3).to(self.device)
            return x / 3 * torch.cos(angle) - y / 3 * torch.sin(angle) + 2 / 3, x / 3 * torch.sin(angle) + y / 3 * torch.cos(angle)

        return [f1, f2, f3, f4]
