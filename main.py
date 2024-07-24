import cv2
import numpy as np
from tkinter import Tk, Button, Scale, HORIZONTAL, filedialog, Label, messagebox
from PIL import Image, ImageTk
import svgwrite

class ImageSegmentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Segmentation Tool")

        self.image = None
        self.segmented_image = None
        self.color_image = None
        self.selected_segments = []

        self.load_button = Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.threshold_label = Label(root, text="Threshold:")
        self.threshold_label.pack()

        self.threshold_scale = Scale(root, from_=0, to_=255, orient=HORIZONTAL, command=self.segment_image)
        self.threshold_scale.pack()

        self.save_button = Button(root, text="Save Segmented Image", command=self.save_image)
        self.save_button.pack()

        self.image_label = Label(root)
        self.image_label.pack()

        self.root.bind("<Button-1>", self.on_click)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.color_image = cv2.imread(file_path)
            if self.image is None or self.color_image is None:
                messagebox.showerror("Error", "Failed to load image!")
                return
            self.display_image(self.image)
            self.segment_image()

    def segment_image(self, val=0):
        if self.image is None:
            return
        threshold_value = self.threshold_scale.get()
        _, self.segmented_image = cv2.threshold(self.image, threshold_value, 255, cv2.THRESH_BINARY)
        self.selected_segments = []
        self.display_image(self.segmented_image)

    def display_image(self, img):
        if img is None:
            return
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if len(img.shape) == 3 else img
        img = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(image=img)
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk

    def on_click(self, event):
        if self.segmented_image is None:
            return
        x = event.x
        y = event.y
        if x < self.segmented_image.shape[1] and y < self.segmented_image.shape[0]:
            mask = np.zeros_like(self.segmented_image)
            mask[self.segmented_image == self.segmented_image[y, x]] = 255
            self.selected_segments.append((mask, self.color_image[y, x]))
            self.highlight_segment(mask)

    def highlight_segment(self, mask):
        highlighted_image = self.segmented_image.copy()
        highlighted_image[mask == 255] = 128
        self.display_image(highlighted_image)

    def save_image(self):
        if not self.selected_segments:
            messagebox.showwarning("Warning", "No segmented part selected!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".svg",
                                                 filetypes=[("SVG files", "*.svg"), ("All files", "*.*")])
        if file_path:
            self.save_svg(file_path)
            messagebox.showinfo("Info", "SVG file saved successfully!")

    def save_svg(self, file_path):
        dwg = svgwrite.Drawing(file_path)
        height, width = self.segmented_image.shape

        for mask, color in self.selected_segments:
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                points = [(point[0][0], point[0][1]) for point in contour]
                color_hex = '#%02x%02x%02x' % (color[2], color[1], color[0])
                dwg.add(dwg.polygon(points, fill=color_hex))

        dwg.save()

if __name__ == "__main__":
    root = Tk()
    app = ImageSegmentationApp(root)
    root.mainloop()


