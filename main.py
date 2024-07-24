import matplotlib.pyplot as plt
import numpy as np
import cv2
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
from tkinter import Tk, Button, filedialog, Label, Toplevel
from PIL import Image, ImageTk
import random
import threading
import time

sam_checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"
device = "cpu"

# Load the SAM model
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
mask_generator = SamAutomaticMaskGenerator(sam)

class MaskSelectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mask Selection Tool")

        self.image = None
        self.masks = None
        self.selected_masks = []

        self.load_button = Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.save_button = Button(root, text="Save Selected Masks", command=self.save_selected_masks)
        self.save_button.pack()

        self.image_label = Label(root)
        self.image_label.pack()

        self.root.bind("<Button-1>", self.on_click)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            if self.image is None:
                return

            # Show loading message
            loading_window = Toplevel(self.root)
            loading_window.title("Loading")
            loading_label = Label(loading_window, text="Masking in progress...")
            loading_label.pack()

            def generate_masks():
                self.masks = mask_generator.generate(self.image)
                self.display_image_with_masks()
                loading_window.destroy()

            threading.Thread(target=generate_masks).start()

    def display_image_with_masks(self):
        img = self.image.copy()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        overlay = img.copy()
        for mask in self.masks:
            color = [random.randint(0, 255) for _ in range(3)]
            overlay[mask['segmentation']] = color

        alpha = 0.5  # Transparency factor.
        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        img = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(image=img)
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk

    def on_click(self, event):
        if self.image is None or self.masks is None:
            return

        x, y = event.x, event.y
        selected_mask = None
        for mask in self.masks:
            if mask['segmentation'][y, x]:
                selected_mask = mask
                break

        if selected_mask:
            self.selected_masks.append(selected_mask)
            self.highlight_selected_masks()

    def highlight_selected_masks(self):
        img = self.image.copy()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        overlay = img.copy()
        for mask in self.masks:
            color = [random.randint(0, 255) for _ in range(3)]
            overlay[mask['segmentation']] = color

        alpha = 0.5  # Transparency factor.
        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        # Highlight selected masks in white, transparent overlay
        for mask in self.selected_masks:
            overlay[mask['segmentation']] = [255, 255, 255]
        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        img = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(image=img)
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk

    def save_selected_masks(self):
        if not self.selected_masks:
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            combined_mask = np.zeros_like(self.image[:, :, 0])
            for mask in self.selected_masks:
                combined_mask = np.bitwise_or(combined_mask, mask['segmentation'].astype(np.uint8))

            cv2.imwrite(file_path, combined_mask * 255)
            print(f"Selected masks saved to {file_path}")

if __name__ == "__main__":
    root = Tk()
    app = MaskSelectionApp(root)
    root.mainloop()





