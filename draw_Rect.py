import sys
import time
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QTimer


class TransparentDrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Transparent Drawing Example')

        # 获取屏幕分辨率
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()

        # 设置窗口大小为屏幕分辨率
        self.setGeometry(screen_rect)

        # 设置窗口背景透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

        # 初始化变量
        self.rectangles = []  # List to store rectangles and their draw times
        self.draw_duration = 3  # Duration in seconds to keep the rectangle on screen

        # Setup a timer to remove rectangles after a certain duration
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.remove_old_rectangles)
        self.timer.start(100)  # Check every 100 milliseconds

    def paintEvent(self, event):
        painter = QPainter(self)
        current_time = time.time()
        for rect, draw_time in self.rectangles:
            if current_time - draw_time <= self.draw_duration:
                self.draw_rect(painter, *rect)

    def draw_rect(self, painter, x, y, width, height):
        painter.setPen(QPen(QColor('blue'), 3))
        painter.drawRect(x, y, width, height)

    def clear(self):
        # Clear the canvas and stop drawing rectangles
        self.rectangles = []
        self.update()  # Trigger repaint

    def draw(self, x, y, width, height):
        # Adjust coordinates and dimensions
        x = 0.6666 * x
        y = 0.6666 * y
        width = 0.6666 * width
        height = 0.6666 * height
        # Add new rectangle with the current time
        self.rectangles.append(((x, y, width, height), time.time()))
        # Enable drawing and trigger repaint
        self.update()  # Trigger repaint
        self.remove_old_rectangles()

    def remove_old_rectangles(self):
        # Remove rectangles that have been on screen longer than the draw duration
        current_time = time.time()
        self.rectangles = [rect for rect in self.rectangles if current_time - rect[1] <= self.draw_duration]
        self.update()  # Trigger repaint


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     widget = TransparentDrawingWidget()
#     # Example: Draw multiple rectangles
#     widget.draw(1924, 800, 346, 30)
#     widget.draw(1924, 500, 346, 30)
#
#     # Example: You can call `widget.clear()` to clear all drawn rectangles
#     # widget.clear()
#
#     widget.show()
#     sys.exit(app.exec())