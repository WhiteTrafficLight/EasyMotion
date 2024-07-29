import time
import mido
import pygame
from PIL import Image, ImageTk
import cv2

def hide_all_masks(app):
    img = app.image.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img_tk = ImageTk.PhotoImage(image=img)
    app.image_label.configure(image=img_tk)
    app.image_label.image = img_tk

def play_midi_and_blink(midi_file, app):
    # Load and play the MIDI file
    pygame.mixer.init()
    pygame.mixer.music.load(midi_file)
    midi_data = mido.MidiFile(midi_file)
    pygame.mixer.music.play()

    for msg in midi_data.play():
        if not app.blinking:
            break
        if msg.type == 'note_on' and msg.velocity > 0:
            highlight_selected_masks(app, brighter=True)
        elif msg.type in ['note_off', 'note_on'] and msg.velocity == 0:
            highlight_selected_masks(app, brighter=False)

    app.blinking = False

def highlight_selected_masks(app, brighter):
    img = app.image.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    overlay = img.copy()
    if brighter:
        # Make the selected masks brighter
        for mask in app.selected_masks:
            overlay[mask['segmentation']] = [255, 255, 255]
    else:
        # Revert the selected masks to their original overlay color
        for mask in app.masks:
            color = [random.randint(0, 255) for _ in range(3)]
            if mask in app.selected_masks:
                overlay[mask['segmentation']] = color

    alpha = 0.5  # Transparency factor.
    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

    img = Image.fromarray(img)
    img_tk = ImageTk.PhotoImage(image=img)
    app.image_label.configure(image=img_tk)
    app.image_label.image = img_tk


