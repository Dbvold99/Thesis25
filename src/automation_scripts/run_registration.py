"""
Runs the image_registration script
"""

from src.preprocessing.image_registration import registrar
from src.utils.os_lib import get_subfolders, make_directory, get_files_from_specific_folder
from get_config import CONFIG

def run_registration():
    list_of_patients_path = get_subfolders(CONFIG['data_paths']['patients'])
    
    for patient_path in list_of_patients_path:
        patient_absolute_path = patient_path.resolve()
        make_directory(patient_absolute_path, CONFIG['patient']['metadata_registered'])
        make_directory(patient_absolute_path, CONFIG['patient']['registered'])

        patient_biopsies = get_files_from_specific_folder(patient_absolute_path, CONFIG['patient']['biopsies'])
        registrar(patient_biopsies, patient_absolute_path)
        

if __name__ == '__main__':
    run_registration()