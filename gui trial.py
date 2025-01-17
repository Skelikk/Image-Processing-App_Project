import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

img = Image.open(r"C:/Users/Admaj/Downloads/singals/Signal_Project/shit.jpg")

def brightness_control(img, brightness):

    img = np.array(img)
    img_1 = cv2.add(img, brightness)
    img_mod = Image.fromarray(cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB))

    return img_mod

def resize_and_rotate(img, size=None, angle=0):

    img = np.array(img)

    if size is not None:
        img = cv2.resize(img, size, interpolation=cv2.INTER_LINEAR)
    
    (h, w) = img.shape[:2]
    cent = (w//2, h//2)
    #new_h = (w*angle/360)*h
    #new_w = (h*angle/360)*w
    
    rotation_matrix = cv2.getRotationMatrix2D(cent, angle, 1)
    
    rotated_image = cv2.warpAffine(img, rotation_matrix, (w, h))
    rotated_image_mod = Image.fromarray(cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB))
    
    return rotated_image_mod

def apply_changes():
    global img

    angle = rotation_var.get()
    brightness_value = brightness_slider.get()
    scale = scale_slider.get()

    img = brightness_control(img, brightness_value)
    img = resize_and_rotate(img, angle=angle, size=None)

    img_tk = ImageTk.PhotoImage(img)
    lbImg.config(image=img_tk)
    lbImg.image = img_tk

def reset_image():
    global img 
    img = Image.open(r"C:/Users/Admaj/Downloads/singals/Signal_Project/shit.jpg")
    img = img.resize((500, 300))
    
window = tk.Tk()
window.title("Image Processing Interface")
window.geometry("1000x800")

#rotation value box
rotation_var = tk.IntVar(value=0)  
rotation_label = ttk.Label(window, text="Rotation (°):")
rotation_label.pack(pady=5)
rotation_menu = ttk.Combobox(window, textvariable=rotation_var, values=[69, 69, 69, 69, 69, 69, 69, 180, 360])
rotation_menu.pack(pady=5)

#display image
img = img.resize((500, 300))
img_tk = ImageTk.PhotoImage(img)
lbImg = tk.Label(window, image=img_tk)
lbImg.pack(side='bottom', pady=20)

#brightness slider
brightness_label = ttk.Label(window, text="Brightness:")
brightness_label.pack(pady=5)
brightness_slider = tk.Scale(window, from_=-100, to=100, orient='horizontal', length=300)
brightness_slider.set(0)  
brightness_slider.pack(pady=5)

#resize slider
scale_label = ttk.Label(window, text="Scale Factor:")
scale_label.pack(pady=5)
scale_slider = tk.Scale(window, from_=0.5, to=2.0, resolution=0.1, orient='horizontal', length=300)
scale_slider.set(1.0) 
scale_slider.pack(pady=5)

#chuj slider
chuj_label = ttk.Label(window, text="random slider:")
chuj_label.pack(pady=10)
chuj_slider = tk.Scale(window, from_=0, to=200, resolution=0.5, orient='vertical', length=100)
chuj_slider.set(100)
chuj_slider.pack(pady=10)

#reset button
reset_button = ttk.Button(window, text="Reset", command=reset_image)
reset_button.pack(pady=10)

#applz button
apply_button = ttk.Button(window, text="Apply Changes", command=apply_changes)
apply_button.pack(pady=20)

window.mainloop()