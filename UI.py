import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QScrollBar, QLabel, QFrame
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import cv2

class ImageUpdater(QThread):
    updated_image = pyqtSignal(QImage)

    def __init__(self, scroll_bars):
        super().__init__()
        self.scroll_bars = scroll_bars
        self.running = True

    def run(self):
        while self.running:
            # Example: Generate a new image based on scroll values
            values = [scroll.value() for scroll in self.scroll_bars]
            image = cv2.imread(r'E:\Desktop\Signals project\Signal_Project\b00_i01_a02_20240813_160158_left_0004.jpg')  # Replace with dynamic image generation based on values
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            self.updated_image.emit(q_image)

    def stop(self):
        self.running = False

class ScrollImageApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scroll Wheels and Image Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create the main layout
        main_layout = QHBoxLayout()

        # Create layout for scroll wheels
        scroll_layout = QVBoxLayout()

        # Add 5 scroll wheels
        self.scroll_bars = []
        for i in range(5):
            scroll = QScrollBar(Qt.Orientation.Vertical)
            scroll.setMinimum(0)
            scroll.setMaximum(100)
            scroll.setValue(50)
            self.scroll_bars.append(scroll)
            scroll_layout.addWidget(scroll)

        # Add scroll wheel layout to main layout
        main_layout.addLayout(scroll_layout)

        # Create image display box
        self.image_frame = QFrame()
        self.image_frame.setFrameShape(QFrame.Shape.Box)
        self.image_frame.setFixedSize(640, 360)

        # Add label for displaying the image
        self.image_label = QLabel(self.image_frame)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add image box to main layout
        main_layout.addWidget(self.image_frame)

        # Set layout for the widget
        self.setLayout(main_layout)

        # Start image update thread
        self.image_thread = ImageUpdater(self.scroll_bars)
        self.image_thread.updated_image.connect(self.update_image)
        self.image_thread.start()

    def update_image(self, q_image):
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))

    def closeEvent(self, event):
        self.image_thread.stop()
        self.image_thread.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScrollImageApp()
    window.show()
    sys.exit(app.exec())
