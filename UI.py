import sys
import os
import pandas as pd
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QSlider, QMessageBox, QSizePolicy, QSpacerItem
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
from skimage.feature import hog
from skimage import exposure
import cv2

class ScrollImageApp(QWidget):

    def __init__(self):
        super().__init__() # Call the __init__ method of the parent class
        self.setWindowTitle("Image Observation Tool For the use of transformation methods")
        self.setGeometry(100, 100, 800, 600)
        self.image_path = None
        self.image_list = []
        self.current_image_index = -1
        self.filters = {
            'greyscale': False,
            'r': False,
            'g': False,
            'b': False,
            'blur': False,
            'edge': False,
            'sift': False,
        } #List of filters to be applied to the image with their default values
        self.image_parameters = pd.DataFrame(columns=[
            'Image Name', 'Greyscale', 'Red', 'Green', 'Blue', 'Blur', 'Blur Value', 'Edge Detection', 'Edge Lower Value', 'Edge Upper Value'
        ]) #DataFrame for storing the parameters of the images
        self.blur_value = 1 #default value for blur filter
        self.edge_lower_value = 1 #Default value for the Lower hysteresis for the edge detection filter
        self.edge_upper_value = 1 #Default value for the Upper hysteresis for the edge detection filter
        self.initUI() #Initialization of the initUI method

    def initUI(self):
        main_layout = QVBoxLayout() #Vertical layout for the main window of the application
        self.setLayout(main_layout)

        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout) 

        image_layout = QVBoxLayout() #Horizontal layout for the image
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored) 
        image_layout.addWidget(self.image_label)       

        parameters_layout = QVBoxLayout() #Vertical layout for the parameters
        self.parameters_label = QLabel("Image Parameters", self)
        self.parameters_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parameters_layout.addWidget(self.parameters_label)

        top_layout.addLayout(image_layout, 4)
        top_layout.addLayout(parameters_layout, 1)

        # Button for the greyscale filter
        self.greyscale_button = QPushButton("Greyscale", self)
        self.greyscale_button.setCheckable(True)
        self.greyscale_button.clicked.connect(lambda: self.toggle_filter('greyscale'))
        parameters_layout.addWidget(self.greyscale_button)

        # Button for the red filter
        self.r_button = QPushButton("R", self)
        self.r_button.setCheckable(True)
        self.r_button.clicked.connect(lambda: self.toggle_filter('r'))
        parameters_layout.addWidget(self.r_button)

        # Button for the green filter
        self.g_button = QPushButton("G", self)
        self.g_button.setCheckable(True)
        self.g_button.clicked.connect(lambda: self.toggle_filter('g'))
        parameters_layout.addWidget(self.g_button)

        # Button for the blue filter
        self.b_button = QPushButton("B", self)
        self.b_button.setCheckable(True)
        self.b_button.clicked.connect(lambda: self.toggle_filter('b'))
        parameters_layout.addWidget(self.b_button)

        # Button for the blur filter
        self.blur_button = QPushButton("Blur", self)
        self.blur_button.setCheckable(True)
        self.blur_button.clicked.connect(lambda: self.toggle_filter('blur'))
        parameters_layout.addWidget(self.blur_button)
    
        # Slider for the blur filter
        self.blur_slider = QSlider(Qt.Orientation.Horizontal)
        self.blur_slider.setRange(1, 50)
        self.blur_slider.setValue(self.blur_value)
        self.blur_slider.valueChanged.connect(self.set_blur_value)
        parameters_layout.addWidget(self.blur_slider)

        # Label for the blur filter slider
        self.blur_value_label = QLabel(str(self.blur_value), self)
        self.blur_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parameters_layout.addWidget(self.blur_value_label)

        # Button for the edge detection filter
        self.edge_button = QPushButton("Edge Detection", self)
        self.edge_button.setCheckable(True)
        self.edge_button.clicked.connect(lambda: self.toggle_filter('edge'))
        parameters_layout.addWidget(self.edge_button)

        # Slider for the lower hysteresis for the edge detection filter
        self.edge_lower_slider = QSlider(Qt.Orientation.Horizontal)
        self.edge_lower_slider.setRange(0, 500)
        self.edge_lower_slider.setValue(self.edge_lower_value)
        self.edge_lower_slider.valueChanged.connect(self.set_edge_lower_value)
        parameters_layout.addWidget(self.edge_lower_slider)

        # Label for the lower hysteresis for the edge detection filter
        self.edge_lower_value_label = QLabel(str(self.edge_lower_value), self)
        self.edge_lower_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parameters_layout.addWidget(self.edge_lower_value_label)

        # Slider for the upper hysteresis for the edge detection filter
        self.edge_upper_slider = QSlider(Qt.Orientation.Horizontal)
        self.edge_upper_slider.setRange(0, 500)
        self.edge_upper_slider.setValue(self.edge_upper_value)
        self.edge_upper_slider.valueChanged.connect(self.set_edge_upper_value)
        parameters_layout.addWidget(self.edge_upper_slider)

        # Label for the upper hysteresis for the edge detection filter
        self.edge_upper_value_label = QLabel(str(self.edge_upper_value), self)
        self.edge_upper_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parameters_layout.addWidget(self.edge_upper_value_label)

        self.sift_button = QPushButton("SIFT", self)
        self.sift_button.setCheckable(True)
        self.sift_button.clicked.connect(lambda: self.toggle_filter('sift'))
        parameters_layout.addWidget(self.sift_button)

        parameters_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        button_layout = QHBoxLayout() #Horizontal layout for the buttons
        main_layout.addLayout(button_layout)

        # Button for choosing an image
        self.choose_image_button = QPushButton("Choose Image", self)
        self.choose_image_button.clicked.connect(self.choose_image)
        button_layout.addWidget(self.choose_image_button)

        # Button for choosing a work folder
        self.choose_folder_button = QPushButton("Choose Folder", self)
        self.choose_folder_button.clicked.connect(self.choose_folder)
        button_layout.addWidget(self.choose_folder_button)

        #Previous button for working in a folder
        self.previous_button = QPushButton("Previous", self)
        self.previous_button.clicked.connect(self.show_previous_image)
        button_layout.addWidget(self.previous_button)

        #Next button for working in a folder
        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.show_next_image)
        button_layout.addWidget(self.next_button)

        self.add_parameters_button = QPushButton("Add Parameters", self)
        self.add_parameters_button.clicked.connect(self.add_parameters)
        button_layout.addWidget(self.add_parameters_button)

        self.save_parameters_button = QPushButton("Save Parameters", self)
        self.save_parameters_button.clicked.connect(self.save_parameters)
        button_layout.addWidget(self.save_parameters_button)

        main_layout.addLayout(button_layout) #Add the button layout to the main layout

    def toggle_filter(self, filter_name): #Method for toggling the filters
        if filter_name in ['r','g','b'] and self.filters['greyscale']:
            self.filters['greyscale'] = False
            self.greyscale_button.setChecked(False)
        elif filter_name in ['greyscale'] and any([self.filters['r'], self.filters['g'], self.filters['b']]):
            self.filters['r'] = False
            self.filters['g'] = False
            self.filters['b'] = False
            self.r_button.setChecked(False)
            self.g_button.setChecked(False)
            self.b_button.setChecked(False)
        self.filters[filter_name] = not self.filters[filter_name]
        self.update_image()

    def set_blur_value(self, value): #Set the value of the blur filter (has to ve an odd number)
        if value % 2 == 1: #If odd set the value
            self.blur_value = value
        else: #if even set the value to the next odd number
            self.blur_value = value + 1
        self.blur_value_label.setText(str(self.blur_value))
        self.update_image()

    def set_edge_lower_value(self, value): #Function for setting the value of the lower hysteresis for the edge detection filter
        self.edge_lower_value = value
        self.edge_lower_value_label.setText(str(self.edge_lower_value))
        self.update_image()

    def set_edge_upper_value(self, value): #Function for setting the value of the upper hysteresis for the edge detection filter
        self.edge_upper_value = value
        self.edge_upper_value_label.setText(str(self.edge_upper_value))
        self.update_image()

    def update_image(self): #Function for updating the image with the selected filters
        if self.image_path:
            image = cv2.imread(self.image_path)
            if self.filters['greyscale']:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if self.filters['r']:
                image[:, :, 0] = 0
                image[:, :, 1] = 0
            if self.filters['g']:
                image[:, :, 0] = 0
                image[:, :, 2] = 0
            if self.filters['b']:
                image[:, :, 1] = 0
                image[:, :, 2] = 0
            if self.filters['blur']:
                image = cv2.GaussianBlur(image, (self.blur_value, self.blur_value), 0)
            if self.filters['edge']:
                image = cv2.Canny(image, self.edge_lower_value, self.edge_upper_value)
            if self.filters['sift']:
                if len(image.shape) == 2:
                    gray = image
                else:
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                sift = cv2.SIFT_create()
                keypoints, descriptors = sift.detectAndCompute(gray, None)
                image = cv2.drawKeypoints(image, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            self.display_image(image)

    def apply_greyscale(self): #Function for applying the greyscale filter
        if self.image_path:
            image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
            self.display_image(image)

    def visualize_sift(self): #SIFT Based on David Lowes paper
        if self.image_path:
            image = cv2.imread(self.image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            sift = cv2.SIFT_create()
            keypoints, descriptors = sift.detectAndCompute(gray, None)
            sift_image = cv2.drawKeypoints(image, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            self.display_image(sift_image)

    def choose_image(self): #Function for choosing an image
        file_dialog = QFileDialog()
        self.image_path, _ = file_dialog.getOpenFileName(self, "Choose Image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if self.image_path:
            self.update_image()

    def choose_folder(self): #Function for choosing a working folder
        file_dialog = QFileDialog()
        folder_path = file_dialog.getExistingDirectory(self, "Choose Folder")
        if folder_path:
            self.image_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
            self.image_list.sort()
            self.current_image_index = 0
            if self.image_list:
                self.image_path = self.image_list[self.current_image_index]
                self.update_image()

    def show_previous_image(self): #Function for showing the previous image in the folder
        if self.image_list and self.current_image_index > 0:
            self.current_image_index -= 1
            self.image_path = self.image_list[self.current_image_index]
            self.update_image()

    def show_next_image(self): #Function for showing the next image in the folder
        if self.image_list and self.current_image_index < len(self.image_list) - 1:
            self.current_image_index += 1
            self.image_path = self.image_list[self.current_image_index]
            self.update_image()

    def add_parameters(self): #Function for adding the parameters of the image to the DataFrame
        if self.image_path:
            image_name = os.path.basename(self.image_path)
            if image_name in self.image_parameters['Image Name'].values:
                reply = QMessageBox.warning(self, "Warning", "Parameters for this image already exist. Do you want to overwrite them?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.No:
                    return
                self.image_parameters = self.image_parameters[self.image_parameters['Image Name'] != image_name]
            new_row = pd.DataFrame([{
                'Image Name': image_name,
                'Greyscale': self.filters['greyscale'],
                'Red': self.filters['r'],
                'Green': self.filters['g'],
                'Blue': self.filters['b'],
                'Blur': self.filters['blur'],
                'Blur Value': self.blur_value if self.filters['blur'] else None,
                'Edge Detection': self.filters['edge'],
                'Edge Lower Value': self.edge_lower_value if self.filters['edge'] else None,
                'Edge Upper Value': self.edge_upper_value if self.filters['edge'] else None
            }])
            self.image_parameters = pd.concat([self.image_parameters, new_row], ignore_index=True)
            print(f"Parameters for {image_name} added: {new_row}")

    def save_parameters(self): #Saving the Parameters from a pandas DataFrame to a CSV file
        if not self.image_parameters.empty:
            file_dialog = QFileDialog()
            save_path, _ = file_dialog.getSaveFileName(self, "Save Parameters", "", "CSV Files (*.csv)")
            if save_path:
                self.image_parameters.to_csv(save_path, index=False, sep=';')
                print(f"Parameters saved to {save_path}")

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