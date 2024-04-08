import matplotlib.pyplot as plt
import numpy as np
import torch
import matplotlib.colors as mcolors
import os
from matplotlib.widgets import Button
from tqdm import tqdm

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class Visualize:
    def __init__(self, points_data: list[torch.Tensor]):
        self.points_data = [i.detach().numpy() for i in points_data]
        self.current_index = 0
        self.playing = True
        self.pre_calculated_colors = self.pre_calculate_colors()
        self.xmin, self.xmax, self.ymin, self.ymax = self.calculate_bounds()
        self.base_interval = 1000  # Base interval in milliseconds
        self.images = self.precompute_images()  # Store precomputed result plots

    def pre_calculate_colors(self):
        # Calculate color gradients once to save time
        all_y_data = np.concatenate([points[1] for points in self.points_data])
        vmin, vmax = np.min(all_y_data), np.max(all_y_data)
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
        linspace = np.linspace(vmin, vmax, 256)
        colors = plt.cm.viridis(norm(linspace))
        return colors, vmin, vmax

    def calculate_bounds(self):
        # Set the display size to the final size to avoid screen resizing each frame
        all_x_data = np.concatenate([points[0] for points in self.points_data])
        all_y_data = np.concatenate([points[1] for points in self.points_data])
        xmin, xmax = np.min(all_x_data), np.max(all_x_data)
        ymin, ymax = np.min(all_y_data), np.max(all_y_data)
        margin = 0.1 * (xmax - xmin)
        return xmin - margin, xmax + margin, ymin - margin, ymax + margin

    def precompute_images(self):
        images = []
        for points in tqdm(self.points_data, desc="Creating Plots"):
            fig, ax = plt.subplots(dpi=700)
            colors = self.calculate_colors(points[0], points[1])
            ax.scatter(points[0], points[1], c=colors, cmap='viridis', s=1)
            ax.set_xlim(self.xmin, self.xmax)
            ax.set_ylim(self.ymin, self.ymax)

            # ax.axis('off')
            fig.canvas.draw()
            image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            images.append(image)

            plt.close(fig)
        return images

    def calculate_colors(self, x_data, y_data):
        # Check and clean data to remove or handle NaNs, infs
        x_data = np.nan_to_num(x_data, nan=0.0, posinf=1.0, neginf=0.0)
        y_data = np.nan_to_num(y_data, nan=0.0, posinf=1.0, neginf=0.0)

        # Normalize x_data and y_data to 0-1 range separately
        epsilon = 10 ** -5
        x_normalized = (x_data - np.min(x_data)) / (np.max(x_data) - np.min(x_data) + epsilon)
        y_normalized = (y_data - np.min(y_data)) / (np.max(y_data) - np.min(y_data) + epsilon)

        # Avoid division by zero or nan results in normalization
        x_normalized = np.nan_to_num(x_normalized, nan=0.5)
        y_normalized = np.nan_to_num(y_normalized, nan=0.5)

        # Combine the normalized x and y values
        combined_normalized = (x_normalized + y_normalized) / 2
        combined_normalized = np.clip(combined_normalized, 0, 1)  # Ensure values are within [0, 1]

        # Map the combined normalized values to colors
        colors, vmin, vmax = self.pre_calculated_colors
        normalized_indices = combined_normalized * (len(colors) - 1)
        normalized_indices = np.clip(normalized_indices, 0, len(colors) - 1).astype(
            int)  # Safeguard against out-of-bound indices

        return colors[normalized_indices]

    def __call__(self):
        # Initialize figure for displaying images
        self.fig, self.ax = plt.subplots(figsize=(10, 8), dpi=200)
        plt.subplots_adjust(bottom=0.1)
        self.img_display = self.ax.imshow(self.images[0])
        self.ax.axis('off')

        axprev = plt.axes([0.59, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.7, 0.05, 0.1, 0.075])
        axplay = plt.axes([0.81, 0.05, 0.1, 0.075])

        bnext = Button(axnext, 'Next')
        bprev = Button(axprev, 'Previous')
        bplay = Button(axplay, 'Pause')

        bnext.on_clicked(self.on_next)
        bprev.on_clicked(self.on_prev)
        bplay.on_clicked(self.on_play_pause)

        self.timer = self.fig.canvas.new_timer(interval=self.base_interval)
        self.timer.add_callback(self.on_next, None)
        self.timer.start()

        plt.show()

    def show_plot(self, index):
        # Update displayed image
        self.img_display.set_data(self.images[index])
        self.ax.set_title(f'Transformed Points at Iteration {index + 1}')
        self.fig.canvas.draw_idle()

    def update_timer_interval(self):
        # Dynamically adjust the timer interval based on the current index to control the speed of automatic navigation
        new_interval = min(self.base_interval * (1.1 ** self.current_index), 4 * self.base_interval)
        self.timer.interval = new_interval

    def on_next(self, event=None):
        # Navigate to the next precomputed image
        self.current_index = (self.current_index + 1) % len(self.images)
        self.show_plot(self.current_index)
        self.update_timer_interval()

    def on_prev(self, event):
        # Navigate to the previous precomputed image
        self.current_index = (self.current_index - 1) % len(self.images)
        self.show_plot(self.current_index)
        # Timer interval update is not necessary for manual navigation

    def on_play_pause(self, event):
        # Toggle the animation play/pause state
        if self.playing:
            self.playing = False
            self.timer.stop()
            event.inaxes.get_children()[0].set_text('Play')
        else:
            self.playing = True
            self.timer.start()
            event.inaxes.get_children()[0].set_text('Pause')
