'''
This module moves all the files from data/raw_scans to data/patients and create patients for each biopsy.
'''

from pathlib import Path
from src.utils.patient_utils import patient_biopsy, move_patients_to_new_folder
from get_config import CONFIG

def associate_biopsies():
    patient_list = patient_biopsy(CONFIG['data_paths']['raw_scans'])
    move_patients_to_new_folder(Path(CONFIG['data_paths']['patients']), patient_list)