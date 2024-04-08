from fractals import Fractal
import torch


class ShrinkingRotating(Fractal):
    max_iterations = 11

    def functions(self):
        def f1(x, y):
            angle = torch.tensor(torch.pi / 6).to(self.device)
            shrink = 1 / 2
            return x * shrink * torch.cos(angle) - y * shrink * torch.sin(angle), x * shrink * torch.sin(angle) + y * shrink * torch.cos(angle)

        def f2(x, y):
            angle = torch.tensor(torch.pi / 6).to(self.device)
            shrink = 1 / 2
            return (x - 1) * shrink * torch.cos(angle) - (y - 1) * shrink * torch.sin(angle) + 1, (x - 1) * shrink * torch.sin(angle) + (y - 1) * shrink * torch.cos(angle) + 1

        def f3(x, y):
            angle = torch.tensor(torch.pi / 3).to(self.device)
            shrink = 1 / 2
            return (x - 1) * shrink * torch.cos(angle) - y * shrink * torch.sin(angle) + 1, x * shrink * torch.sin(angle) + y * shrink * torch.cos(angle)

        def f4(x, y):
            angle = torch.tensor(torch.pi / 3).to(self.device)
            shrink = 1 / 2
            return x * shrink * torch.cos(angle) - y * shrink * torch.sin(angle), (x - 1) * shrink * torch.sin(angle) + (y - 1) * shrink * torch.cos(angle) + 1

        return [f1, f2, f3, f4]
