from src.preprocessing.patches_generation import generate_coords_no_overlap, is_patch_mostly_black, save_patches, rebuild_image
import argparse
import numpy as np
import json
from pathlib import Path
from src.utils.os_lib import make_directory
from get_config import CONFIG
from PIL import Image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--patient_dir", type=str, required=True, help="Path to patient folder")
    parser.add_argument("--tissue_mask_path", type=str, required=True, help="Path to binary tissue mask")

    args = parser.parse_args()

    patient_path = Path(args.patient_dir)
    binary_mask = Path(args.tissue_mask_path)

    patch_size = 24
    black_threshold = 0.9 

    make_directory(patient_path, CONFIG['patient']['patches'])

    image = np.array(Image.open(f"{binary_mask}"))
    if image.ndim == 2:
        image = np.stack([image]*3, axis=-1)
    
    save_dir = patient_path / CONFIG['patient']['patches']
    coords = generate_coords_no_overlap(image.shape[:2], patch_size)
    metadata = save_patches(image, coords, save_dir, black_threshold=black_threshold)
    json_output_path = patient_path / CONFIG['patient']['patches_metadata']

    with open(json_output_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    reconstructed = rebuild_image(json_output_path, save_dir, image.shape[:2])
    Image.fromarray(reconstructed).save(patient_path /'reconstructed_image.png')

if __name__ == '__main__':
    main()