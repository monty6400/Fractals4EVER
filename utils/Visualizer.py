import numpy as np
import torch
from utils.ImageViewer import displayImage

class Visualize:
    def __init__(self, image_size, points_data: list[torch.Tensor]):
        points = []
        for tensor in points_data:
            if tensor.shape[0] == 2:
                pairs = tensor.transpose(0, 1).numpy()
                points.extend(pairs)
        self.points = np.array(points)
        self.image_size = image_size

    def scale_points(self):
        # Convert points to a NumPy array
        min_val = np.min(self.points, axis=0)
        max_val = np.max(self.points, axis=0)

        # Target range within the image
        min_target = 0.1 * self.image_size
        max_target = 0.9 * self.image_size

        # Scale points to the range 10% to 90% of the image dimensions
        scaled_points = ((self.points - min_val) / (max_val - min_val)) * (max_target - min_target) + min_target
        scaled_points = (self.image_size, 0.0) - scaled_points
        return scaled_points.astype(int)

    def create_image(self):
        # Initialize the image array with zeros (black)
        image = np.zeros((self.image_size, self.image_size, 3), dtype=np.uint8)

        # Scale the points
        scaled_points = self.scale_points()

        # Convert scaled points to integer and separate x and y coordinates
        xs, ys = scaled_points[:, 0], scaled_points[:, 1]

        # Set the corresponding pixels to white more efficiently using array indexing
        image[ys, xs] = [255, 255, 255]

        return image

    def show(self, max_size=1024):
        image = self.create_image()
        image_zoomer = displayImage(image, max_size=max_size)
        image_zoomer.displayImage()



