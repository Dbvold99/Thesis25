"""
This module create patches from an input image
"""

import os
import json
import numpy as np
from PIL import Image
from tqdm import tqdm

# Allow handling very large images
Image.MAX_IMAGE_PIXELS = None

def generate_coords_no_overlap(image_shape, patch_size):

    h, w = image_shape
    xs = list(range(0, w - patch_size + 1, patch_size))
    ys = list(range(0, h - patch_size + 1, patch_size))
    if xs[-1] != w - patch_size:
        xs.append(w - patch_size)
    if ys[-1] != h - patch_size:
        ys.append(h - patch_size)

    coords = []
    for y in ys:
        for x in xs:
            coords.append({
                "x_start": x,
                "y_start": y,
                "x_end":   x + patch_size,
                "y_end":   y + patch_size
            })
    return coords

def is_patch_mostly_black(patch, black_threshold=0.9):
    """
    Returns True if the patch is considered mostly black.
    A patch is skipped if more than `black_threshold` of pixels are black (value = 0).
    """
    if patch.ndim == 3:
        gray = np.mean(patch, axis=2)
    else:
        gray = patch

    black_fraction = np.mean(gray < 5)
    return black_fraction >= black_threshold

import numpy as np

def is_patch_mostly_white(patch, white_threshold=0.9):
    """
    Returns True if the patch is considered mostly white.
    A patch is considered mostly white if more than `white_threshold` of pixels are white (value ≈ 255).
    """
    if patch.ndim == 3:
        gray = np.mean(patch, axis=2)
    else:
        gray = patch

    white_fraction = np.mean(gray > 240)
    return white_fraction >= white_threshold

def save_patches(image, coords, save_dir, black_threshold=0.9):
    '''
    Stores the patches in a json file. A patch is represented by:
        x_start, y_start: The topleft corner
        x_end, y_end: The bottomright corner
        name of patch
    '''
    os.makedirs(save_dir, exist_ok=True)
    metadata = []

    for idx, coord in enumerate(tqdm(coords, desc="Saving patches")):
        x0, y0 = coord["x_start"], coord["y_start"]
        x1, y1 = coord["x_end"],   coord["y_end"]
        patch = image[y0:y1, x0:x1]

        if patch.size == 0 or is_patch_mostly_black(patch, black_threshold):
            continue

        fname = f"patch_{idx:04d}.png"
        Image.fromarray(patch).convert('RGB').save(os.path.join(save_dir, fname))

        meta = {
            "x_start": x0,
            "y_start": y0,
            "x_end":   x1,
            "y_end":   y1,
            "filename": fname
        }
        metadata.append(meta)

    return metadata




def rebuild_image(json_path, patch_folder, original_shape):
    with open(json_path, 'r') as f:
        metadata = json.load(f)

    h, w = original_shape
    reconstructed = np.zeros((h, w, 3), dtype=np.uint8)

    for entry in metadata:
        patch = np.array(Image.open(os.path.join(patch_folder, entry["filename"])))
        x0, y0 = entry["x_start"], entry["y_start"]
        x1, y1 = entry["x_end"],   entry["y_end"]
        reconstructed[y0:y1, x0:x1, :] = patch

    return reconstructed




def rebuild_image_stain(output_dir, patch_folder, original_shape):
    with open(output_dir / 'metadata.json', 'r') as f:
        metadata = json.load(f)

    h, w = original_shape
    reconstructed = np.zeros((h, w, 3), dtype=np.uint8)

    for entry in metadata:
        patch = np.array(Image.open(os.path.join(patch_folder, entry["filename"])))
        x0, y0 = entry["x_start"], entry["y_start"]
        x1, y1 = entry["x_end"],   entry["y_end"]
        reconstructed[y0:y1, x0:x1, :] = patch

    return reconstructed