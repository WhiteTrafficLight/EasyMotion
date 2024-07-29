import threading
from tkinter import Button, Label, Toplevel, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import random
import numpy as np

from .sam_model import load_sam_model, generate_masks
from .utils import play_midi_and_blink, hide_all_masks

sam, mask_generator = load_sam_model()

class MaskSelectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mask Selection Tool")

        self.image = None
        self.masks = None
        self.selected_masks = []
        self.blinking = False

        self.load_button = Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.save_button = Button(root, text="Save Selected Masks", command=self.save_selected_masks)
        self.save_button.pack()

        self.done_button = Button(root, text="Done", command=self.start_midi_blinking)
        self.done_button.pack()

        self.renew_button = Button(root, text="Renew", command=self.renew_masks)
        self.renew_button.pack()

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

            def generate_masks_thread():
                self.masks = generate_masks(mask_generator, self.image)
                self.display_image_with_masks()
                loading_window.destroy()

            threading.Thread(target=generate_masks_thread).start()

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

        messagebox.showinfo("Info", "Select the masks you want to hypnotize.")

    def on_click(self, event):
        if self.image is None or self.masks is None:
            return

        x, y = event.x, event.y
        selected_mask = None
        for mask in self.masks:
            if mask['segmentation'][y, x]:
                selected_mask = mask
                break

        if selected_mask and selected_mask not in self.selected_masks:
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

    def start_midi_blinking(self):
        file_path = filedialog.askopenfilename(filetypes=[("MIDI files", "*.mid"), ("All files", "*.*")])
        if file_path:
            self.blinking = True
            hide_all_masks(self)
            threading.Thread(target=play_midi_and_blink, args=(file_path, self)).start()

    def renew_masks(self):
        self.selected_masks = []
        self.highlight_selected_masks()



