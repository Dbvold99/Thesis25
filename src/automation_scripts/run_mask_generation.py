"""
Runs the mask_generation
"""

from src.preprocessing.mask_generation import mask_binary, save_mask
from src.utils.os_lib import get_subfolders, make_directory
from get_config import CONFIG

def run_mask_generation():

    list_of_patients_path = get_subfolders(CONFIG['data_paths']['patients'])

    for patient_path in list_of_patients_path:
        patient_absolute_path = patient_path.resolve()
        path_non_rigid_overlap_biopsy = patient_absolute_path / CONFIG['patient']['non_rigid_overlap_biopsy']

        red_mask, green_mask, blue_mask, cleaned_matched_mask, watershed_mask = mask_binary(path_non_rigid_overlap_biopsy)

        make_directory(patient_absolute_path, CONFIG['patient']['binary_tissue_masks'])

        mask_output_dir = patient_absolute_path / CONFIG['patient']['binary_tissue_masks']
        save_mask(red_mask, mask_output_dir, "red_mask")
        save_mask(green_mask, mask_output_dir, "green_mask")
        save_mask(blue_mask, mask_output_dir, "blue_mask")
        save_mask(cleaned_matched_mask, mask_output_dir, "tissue_mask")
        save_mask(watershed_mask, mask_output_dir, "watershed_mask", scale=False)




if __name__ == '__main__':
    run_mask_generation()