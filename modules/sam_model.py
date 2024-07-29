import torch
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator

sam_checkpoint = "./sam_vit_h_4b8939.pth"
model_type = "vit_h"
device = "cpu"

def load_sam_model():
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)
    mask_generator = SamAutomaticMaskGenerator(sam)
    return sam, mask_generator

def generate_masks(mask_generator, image):
    return mask_generator.generate(image)