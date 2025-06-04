from src.preprocessing.mask_generation import mask_binary, save_mask
import argparse
from pathlib import Path
from src.utils.os_lib import make_directory
from get_config import CONFIG




def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--patient_dir", type=str, required=True, help="Path to patient folder")
    parser.add_argument("--registration", type=str, help="path to rigid overlap")

    args = parser.parse_args()

    patient_path = Path(args.patient_dir)

    overlap_non_rigid = Path(args.registration)

    make_directory(patient_path, CONFIG['patient']['binary_tissue_masks'])

    red_mask, green_mask, blue_mask, cleaned_mask, watershed_mask= mask_binary(overlap_non_rigid)

    mask_output_dir = patient_path / CONFIG['patient']['binary_tissue_masks']
    save_mask(red_mask, mask_output_dir, "red_mask")
    save_mask(green_mask, mask_output_dir, "green_mask")
    save_mask(blue_mask, mask_output_dir, "blue_mask")
    save_mask(cleaned_mask, mask_output_dir, "tissue_mask")
    save_mask(watershed_mask, mask_output_dir, "watershed_mask", scale=False)


if __name__ == '__main__':
    main()