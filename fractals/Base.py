import os
import pickle
import sys

import torch
from tqdm import tqdm


class Fractal:
    max_iterations = 0

    def __init__(self, initial_points, iter_num=0, enforce_iter=False, save_path=None):
        # Check for GPU availability
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.save_path = save_path
        self.iter_num = iter_num if iter_num else self.max_iterations
        self.points = torch.tensor(initial_points).to(self.device)
        self.points_data = [self.points.clone().to(self.device)]

        if self.iter_warning():
            if enforce_iter:
                self.iter_num = self.max_iterations
            else:
                print(f"\033[93mWarning: iteration number is high, recommended not to surpass {self.max_iterations}")

    def iterate(self):
        if self.load_if_exists():
            return

        for i in tqdm(range(self.iter_num), desc="Calculating Fractal"):
            U_final = torch.tensor([], dtype=torch.float, device=self.device)
            V_final = torch.tensor([], dtype=torch.float, device=self.device)
            for f in self.functions():
                U, V = f(self.points[0], self.points[1])
                U_final = torch.cat((U_final, U))
                V_final = torch.cat((V_final, V))
            self.points = torch.stack([U_final, V_final])
            # Convert points to numpy array for unique operation
            unique_points = {tuple(point.cpu().numpy()) for point in self.points.t()}
            self.points = torch.tensor(list(unique_points), dtype=torch.float, device=self.device).t()
            self.points_data.append(self.points)
        self.points_data = [i.to('cpu') for i in self.points_data]

        if self.save_path:
            self.save()

    def functions(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def iter_warning(self):
        return self.iter_num > self.max_iterations

    def get_save_path(self):
        return os.path.join(self.save_path, self.__class__.__name__)

    def load_if_exists(self):
        if self.save_path:
            save_dir = self.get_save_path()
            file_path = os.path.join(save_dir, f"iter_{self.iter_num}.pickle")
            if os.path.exists(file_path):
                for _ in tqdm(range(1), desc="Loading Precomputed Fractal"):
                    with open(file_path, 'rb') as f:
                        self.points_data = pickle.load(f)
                return True
        return False

    def save(self):
        save_dir = self.get_save_path()
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, f"iter_{self.iter_num}.pickle")
        with open(file_path, 'wb') as f:
            pickle.dump(self.points_data, f)
            