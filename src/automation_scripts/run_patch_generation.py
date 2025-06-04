"""
Runs the patches_generation script
"""

from src.preprocessing.patches_generation import generate_coords_no_overlap, save_patches, rebuild_image
from src.utils.os_lib import get_subfolders
import numpy as np
import json
from get_config import CONFIG
from PIL import Image


def run_patch_generation():
    list_of_patients_path = get_subfolders(CONFIG['data_paths']['patients'])
    patch_size = 24
    black_threshold = 0.9 

    for patient_path in list_of_patients_path:
        patient_absolute_path = patient_path.resolve()
        path_tissue_mask = patient_absolute_path / CONFIG['patient']['tissue_mask']

        save_dir = patient_absolute_path / CONFIG['patient']['patches']
        json_output_path = patient_absolute_path / CONFIG['patient']['patches_metadata']

        image = np.array(Image.open(path_tissue_mask))
        if image.ndim == 2:
            image = np.stack([image]*3, axis=-1)

        coords = generate_coords_no_overlap(image.shape[:2], patch_size)
        metadata = save_patches(image, coords, save_dir, black_threshold=black_threshold)

        with open(json_output_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        reconstructed = rebuild_image(json_output_path, save_dir, image.shape[:2])
        Image.fromarray(reconstructed).save(patient_absolute_path /'reconstructed_image.png')
        print("Reconstruction complete.")

if __name__ == "__main__":
    run_patch_generation()
