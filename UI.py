import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QScrollBar, QLabel, QFrame, QLineEdit, QPushButton, QFileDialog, QSlider
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMutex
import cv2

class ScrollImageApp(QWidget):

    def __init__(self):
        super().__init__() # Call the __init__ method of the parent class
        self.setWindowTitle("Image Observation Tool For the use of transformation methods")
        self.setGeometry(100, 100, 800, 600)
        self.image_path = None
        self.filters = {
            'greyscale': False,
            'colour': False,
            'r': False,
            'g': False,
            'b': False,
            'blur': False,
            'edge': False
        } #List of filters to be applied to the image with their default values
        self.blur_value = 1 #default value for blur filter
        self.edge_lower_value = 1 #Default value for the Lower hysteresis for the edge detection filter
        self.edge_upper_value = 1 #Default value for the Upper hysteresis for the edge detection filter
        self.initUI() #Initialization of the initUI method

    def initUI(self):
        layout = QVBoxLayout() #Vertical layout for the main window of the application
        self.setLayout(layout) 

        self.image_label = QLabel(self) 
        layout.addWidget(self.image_label) #Add the image label to the layout

        button_layout = QHBoxLayout() #Horizontal layout for the buttons

        # Button for the greyscale filter
        self.greyscale_button = QPushButton("Greyscale", self)
        self.greyscale_button.setCheckable(True)
        self.greyscale_button.clicked.connect(lambda: self.toggle_filter('greyscale'))
        button_layout.addWidget(self.greyscale_button)

        # Button for the colour filter
        self.colour_button = QPushButton("Colour", self)
        self.colour_button.setCheckable(True)
        self.colour_button.clicked.connect(lambda: self.toggle_filter('colour'))
        button_layout.addWidget(self.colour_button)

        # Button for the red filter
        self.r_button = QPushButton("R", self)
        self.r_button.setCheckable(True)
        self.r_button.clicked.connect(lambda: self.toggle_filter('r'))
        button_layout.addWidget(self.r_button)

        # Button for the green filter
        self.g_button = QPushButton("G", self)
        self.g_button.setCheckable(True)
        self.g_button.clicked.connect(lambda: self.toggle_filter('g'))
        button_layout.addWidget(self.g_button)

        # Button for the blue filter
        self.b_button = QPushButton("B", self)
        self.b_button.setCheckable(True)
        self.b_button.clicked.connect(lambda: self.toggle_filter('b'))
        button_layout.addWidget(self.b_button)

        # Button for the blur filter
        self.blur_button = QPushButton("Blur", self)
        self.blur_button.setCheckable(True)
        self.blur_button.clicked.connect(lambda: self.toggle_filter('blur'))
        button_layout.addWidget(self.blur_button)
    
        # Slider for the blur filter
        self.blur_slider = QSlider(Qt.Orientation.Horizontal)
        self.blur_slider.setRange(1, 20)
        self.blur_slider.setValue(self.blur_value)
        self.blur_slider.valueChanged.connect(self.set_blur_value)
        button_layout.addWidget(self.blur_slider)

        # Button for the edge detection filter
        self.edge_button = QPushButton("Edge Detection", self)
        self.edge_button.setCheckable(True)
        self.edge_button.clicked.connect(lambda: self.toggle_filter('edge'))
        button_layout.addWidget(self.edge_button)

        # Slider for the lower hysteresis for the edge detection filter
        self.edge_lower_slider = QSlider(Qt.Orientation.Horizontal)
        self.edge_lower_slider.setRange(0, 100)
        self.edge_lower_slider.setValue(self.edge_lower_value)
        self.edge_lower_slider.valueChanged.connect(self.set_edge_lower_value)
        button_layout.addWidget(self.edge_lower_slider)

        # Slider for the upper hysteresis for the edge detection filter
        self.edge_upper_slider = QSlider(Qt.Orientation.Horizontal)
        self.edge_upper_slider.setRange(0, 100)
        self.edge_upper_slider.setValue(self.edge_upper_value)
        self.edge_upper_slider.valueChanged.connect(self.set_edge_upper_value)
        button_layout.addWidget(self.edge_upper_slider)

        # Button for choosing an image
        self.choose_image_button = QPushButton("Choose Image", self)
        self.choose_image_button.clicked.connect(self.choose_image)
        button_layout.addWidget(self.choose_image_button)

        # Button for choosing a work folder
        self.choose_folder_button = QPushButton("Choose Folder", self)
        self.choose_folder_button.clicked.connect(self.choose_folder)
        button_layout.addWidget(self.choose_folder_button)

        layout.addLayout(button_layout) #Add the button layout to the main layout

    def toggle_filter(self, filter_name): #Method for toggling the filters
        self.filters[filter_name] = not self.filters[filter_name]
        self.update_image()

    def set_blur_value(self, value): #Set the value of the blur filter (has to ve an odd number)
        if value % 2 == 1: #If odd set the value
            self.blur_value = value
        else: #if even set the value to the next odd number
            self.blur_value = value + 1
        self.update_image()

    def set_edge_lower_value(self, value): #Function for setting the value of the lower hysteresis for the edge detection filter
        self.edge_lower_value = value
        self.update_image()

    def set_edge_upper_value(self, value): #Function for setting the value of the upper hysteresis for the edge detection filter
        self.edge_upper_value = value
        self.update_image()

    def update_image(self): #Function for updating the image with the selected filters
        if self.image_path:
            image = cv2.imread(self.image_path)
            if self.filters['greyscale']:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if self.filters['colour']:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            if self.filters['r']:
                image[:, :, 1] = 0
                image[:, :, 2] = 0
            if self.filters['g']:
                image[:, :, 0] = 0
                image[:, :, 2] = 0
            if self.filters['b']:
                image[:, :, 0] = 0
                image[:, :, 1] = 0
            if self.filters['blur']:
                image = cv2.GaussianBlur(image, (self.blur_value, self.blur_value), 0)
            if self.filters['edge']:
                image = cv2.Canny(image, self.edge_lower_value, self.edge_upper_value)
            self.display_image(image)

    def apply_greyscale(self): #Function for applying the greyscale filter
        if self.image_path:
            image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
            self.display_image(image)

    def choose_image(self): #Function for choosing an image
        file_dialog = QFileDialog()
        self.image_path, _ = file_dialog.getOpenFileName(self, "Choose Image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if self.image_path:
            self.update_image()

    def choose_folder(self): #Function for choosing a working folder
        file_dialog = QFileDialog()
        folder_path = file_dialog.getExistingDirectory(self, "Choose Folder")
        if folder_path:
            print(f"Selected folder: {folder_path}")

    def display_image(self, image): #Function for displaying the image with conversion from opencv to QImage
        if image is not None:
            if len(image.shape) == 2:
                q_image = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format.Format_Grayscale8)
            else:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                q_image = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(q_image))

# Main function for running the application (Needs to always be added to the end of the script) (Be aware when modifying!)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScrollImageApp()
    window.show()
    sys.exit(app.exec())