from src.preprocessing.patches_generation import save_patches, generate_coords_no_overlap, rebuild_image_stain
from src.utils.os_lib import get_subfolders, get_files_in_folder, make_directory
from get_config import CONFIG

from PIL import Image
import numpy as np
import json
from pathlib import Path


def main():
    list_of_patients_path = get_subfolders(CONFIG['data_paths']['patients'])
    patch_size = 1024

    for patient_path in list_of_patients_path:
        patient_absolute_path = patient_path.resolve()

        make_directory(patient_absolute_path, CONFIG['patient']['patches'])
        make_directory(patient_absolute_path, CONFIG['patient']['HE_patches'])
        make_directory(patient_absolute_path, CONFIG['patient']['ki67_patches'])
        make_directory(patient_absolute_path, CONFIG['patient']['psa_patches'])

        path_to_registered = get_files_in_folder(str(patient_absolute_path / CONFIG['patient']['registered']))

        for idx, registered_path in enumerate(path_to_registered):
            if idx == 0:
                output_dir = patient_absolute_path / CONFIG['patient']['HE_patches']
            elif idx == 1:
                output_dir = patient_absolute_path / CONFIG['patient']['ki67_patches']
            elif idx == 2:
                output_dir = patient_absolute_path / CONFIG['patient']['psa_patches']
            else:
                print(f"More than 3 registered images found for {patient_absolute_path.name}, aborting...")
                break

            image = np.array(Image.open(registered_path))
            if image.ndim == 2:
                image = np.stack([image] * 3, axis=-1)

            coords = generate_coords_no_overlap(image.shape[:2], patch_size)
            metadata = save_patches(image, coords, output_dir, 0.9)

            with open(output_dir / 'metadata.json', 'w') as f:
                json.dump(metadata, f, indent=2)

            reconstructed = rebuild_image_stain(output_dir, output_dir, image.shape[:2])
            Image.fromarray(reconstructed).save(output_dir / 'reconstructed_image.png')


if __name__ == '__main__':
    main()