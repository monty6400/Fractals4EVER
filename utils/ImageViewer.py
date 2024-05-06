import numpy as np
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QImage, QWheelEvent
from PyQt5.QtCore import Qt, QPoint
import sys
from PIL import Image


class ImageZoomer(QMainWindow):
    def __init__(self, image, max_size=1024):
        super().__init__()
        self.max_size = max_size
        if isinstance(image, np.ndarray):
            self.image = Image.fromarray(image)
        else:
            self.image = Image.open(image)
        self.zoom_level = 1
        self.current_x = 0
        self.current_y = 0
        self.current_width = self.image.width
        self.current_height = self.image.height

        self.setMouseTracking(True)  # Enable mouse tracking
        self.dragging = False

        self.initUI()

    def initUI(self):
        aspect_ratio = self.image.width / self.image.height

        window_width = self.max_size
        window_height = self.max_size
        if aspect_ratio >= 1:
            window_height = round(window_height / aspect_ratio)
        else:
            window_width = round(window_width / aspect_ratio)

        self.setFixedWidth(window_width)
        self.setFixedHeight(window_height)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)
        self.updateImage()
        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.mouse_click_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            drag_delta = event.pos() - self.mouse_click_point
            self.mouse_click_point = event.pos()
            # print(drag_delta)
            self.dragImage(drag_delta)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False

    def wheelEvent(self, event: QWheelEvent):
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            # cursor_pos = event.pos()
            # image_rect = self.label.contentsRect()

            # relative_x = cursor_pos.x() / image_rect.width()
            # relative_y = cursor_pos.y() / image_rect.height()

            relative_x = 0.5
            relative_y = 0.5
            # Calculate factor by which to zoom
            zoom_factor = 1.05 if event.angleDelta().y() > 0 else 0.95

            # New zoom level, limited to a sensible range
            self.zoom_level = max(1.0, min(40.0, self.zoom_level * zoom_factor))

            # Update the image with zoom focused on cursor
            self.zoomOnImage(focus_point=(relative_x, relative_y))

    def zoomOnImage(self, focus_point=(0, 0)):
        width, height = self.image.size

        scaled_width = int(width / self.zoom_level)
        scaled_height = int(height / self.zoom_level)

        # Calculate the new focus point's location on the original image
        original_focus_x = focus_point[0] * self.current_width + self.current_x
        original_focus_y = focus_point[1] * self.current_height + self.current_y

        # Calculate the new top-left corner of the image portion to display
        new_x = original_focus_x - scaled_width // 2
        new_y = original_focus_y - scaled_height // 2

        # Ensure the new coordinates are within bounds
        new_x = int(max(0, min(width - scaled_width, new_x)))
        new_y = int(max(0, min(height - scaled_height, new_y)))

        # print(new_x, new_y, scaled_width, scaled_height)
        # print(self.current_x, self.current_y, self.current_width, self.current_height)
        # Crop the image based on new top-left corner and zoom level
        self.current_x = new_x
        self.current_y = new_y
        self.current_width = scaled_width
        self.current_height = scaled_height
        self.updateImage()

    def dragImage(self, dragDelta: QPoint):
        self.current_x -= dragDelta.x()*6*self.current_width/self.image.width
        self.current_y -= dragDelta.y()*6*self.current_height/self.image.height

        self.current_x = max(0, min(self.current_x, self.image.width - self.current_width))
        self.current_y = max(0, min(self.current_y, self.image.height - self.current_height))

        self.updateImage()


    def updateImage(self):
        rect_width = self.width()
        rect_height = self.height()
        cropped_image = self.image.crop((int(self.current_x), int(self.current_y),
                                         int(self.current_x + self.current_width),
                                         int(self.current_y + self.current_height))).resize((rect_width, rect_height))
        qt_image = QImage(cropped_image.tobytes(), cropped_image.width, cropped_image.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)

        self.label.setPixmap(pixmap.scaled(pixmap.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

def displayImage(image, max_size=1024):
    app = QApplication(sys.argv)
    ex = ImageZoomer(image, max_size)
    sys.exit(app.exec_())


if __name__ == '__main__':
    displayImage("1.jpg")