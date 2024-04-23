import tkinter as tk
from tkinter import filedialog, messagebox
import cv2

class ImageToSketchConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Sketch Converter")
        
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.upload_button = tk.Button(self.root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.convert_button = tk.Button(self.root, text="Convert to Sketch", command=self.convert_to_sketch)
        self.convert_button.pack()

        self.save_button = tk.Button(self.root, text="Save Sketch", command=self.save_sketch)
        self.save_button.pack()

        self.line_thickness_label = tk.Label(self.root, text="Line Thickness")
        self.line_thickness_label.pack()
        self.line_thickness_slider = tk.Scale(self.root, from_=1, to=10, orient="horizontal")
        self.line_thickness_slider.pack()

        self.contrast_label = tk.Label(self.root, text="Contrast")
        self.contrast_label.pack()
        self.contrast_slider = tk.Scale(self.root, from_=0.1, to=2.0, resolution=0.1, orient="horizontal")
        self.contrast_slider.pack()

        self.brightness_label = tk.Label(self.root, text="Brightness")
        self.brightness_label.pack()
        self.brightness_slider = tk.Scale(self.root, from_=-100, to=100, orient="horizontal")
        self.brightness_slider.pack()

    def upload_image(self):
        self.filepath = filedialog.askopenfilename()
        if self.filepath:
            self.image = cv2.imread(self.filepath)
            self.display_image()

    def display_image(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image = cv2.resize(self.image, (400, 400))
        self.photo = tk.PhotoImage(data=cv2.imencode('.png', self.image)[1].tobytes())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def convert_to_sketch(self):
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        inverted_gray_image = 255 - gray_image
        blurred_image = cv2.GaussianBlur(inverted_gray_image, (21, 21), sigmaX=0, sigmaY=0)
        inverted_blurred_image = 255 - blurred_image
        self.sketch = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)
        self.adjust_parameters()

    def adjust_parameters(self):
        line_thickness = self.line_thickness_slider.get()
        contrast = self.contrast_slider.get()
        brightness = self.brightness_slider.get()

        self.sketch = cv2.multiply(self.sketch, contrast)
        self.sketch = cv2.add(self.sketch, brightness)

        self.display_sketch()

    def display_sketch(self):
        self.sketch = cv2.resize(self.sketch, (400, 400))
        self.photo = tk.PhotoImage(data=cv2.imencode('.png', self.sketch)[1].tobytes())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def save_sketch(self):
        if hasattr(self, 'sketch'):
            save_path = filedialog.asksaveasfilename(defaultextension=".png")
            if save_path:
                cv2.imwrite(save_path, self.sketch)
                messagebox.showinfo("Success", "Sketch saved successfully!")
        else:
            messagebox.showerror("Error", "No sketch to save!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToSketchConverter(root)
    root.mainloop()
