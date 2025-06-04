'''
This sub-module is for creating a patient object and associate raw_scans with correct patient. 

Following functions exists:
    
create_patient(id: int, he_scan: Path, ki67_scan: Path, psa_scan: Path) -> Patient
    Takes a id that is generated in patient biopsiy.
    All the paths to the scans, that is folder 'raw_scans'.

has_patient_all_biopsies(biopsies: List[int]) -> bool:
    Checks if a patient has all biopsies. Currently, on the dropbox a patient has all biopsies if
    three files exists that is incremented by one. Example: 120.npdi, 121.npdi, 122.npdi is a patient.

patient_biopsy(folder:str) -> Dict[int, Patient]:
    iterates through 'raw_scans' folder and creates a Dictionary with all patients and their associated 
    biopsies. #TODO: Handle error, if 'raw_scans' has an error, e.g. one biopsy is missing, the code will
    *not* work.

move_patients_to_new_folder(new_folder: Path, all_patients: Dict[int, Patient])
    Iterathes through all the patients and create a new folder for each patient and move the biopsies from
    'raw_scans' to the new folder.
'''


from pathlib import Path
from typing import List, Dict
import shutil

from src.utils.patient_class import Patient
from src.utils.os_lib import numerically_sort_files_in_folder, get_numbers, count_subfolders
from get_config import CONFIG


def create_patient(id: int, he_scan: Path, ki67_scan: Path, psa_scan: Path) -> Patient:
    '''
    creates a patient object
    '''

    return Patient(id, he_scan, ki67_scan, psa_scan)




def has_patient_all_biopsies(biopsies: List[int]) -> bool:
    '''
    Checks if it a sequential order 
    Example: 1,2,3 returns True
            1,3,2 returns False
    '''

    if (biopsies[0] == biopsies[1] - 1) and (biopsies[0] == biopsies[2] - 2):
        return True
    else:
        return False




def patient_biopsy(folder:str) -> Dict[int, Patient]:
    '''
    Pathologist has labeled biopsies as following:
        1_scan.npdi <- H&E from patient A
        2_scan.npdi <- Ki67 from patient A
        3_scan.npdi <- PSA from patient A
        11_scan.npdi <- H&E from patient B
        12_scan.npdi <- Ki67 from patient B
        13_scan.npdi <- PSA from patient B
    create a Patient according to the labeling.
    '''
    path_raw_scans = numerically_sort_files_in_folder(folder)
    number_of_existing_patients = count_subfolders(Path(CONFIG['data_paths']['patients']))
    patient_id = number_of_existing_patients
        
    all_patients = {}

    for patient_biopsies in range (0, len(path_raw_scans), 3):
        all_biopsies = path_raw_scans[patient_biopsies:patient_biopsies + 3]
        patient_id += 1

        if has_patient_all_biopsies(get_numbers(all_biopsies)):
            new_patient = Patient(patient_id, all_biopsies[0], all_biopsies[1], all_biopsies[2])
            all_patients[patient_id] = new_patient
        else:
            continue
    
    return all_patients



def move_patients_to_new_folder(new_folder: Path, all_patients: Dict[int, Patient]) -> None:
    '''
    Moves biopsy files (H&E, Ki67, PSA) for each patient into a new folder structure.
    
    For each patient, creates a subfolder named 'patient_{patient_id}' and moves their associated biopsy files there.
    '''
    for patient_id in sorted(all_patients.keys()):
        patient = all_patients[patient_id]

        patient_folder = new_folder / f"patient_{patient_id}"
        patient_folder.mkdir(parents=True, exist_ok=True)

        biopsy_files = [
            (patient.he_scan, "_HE"),
            (patient.ki67_scan, "_Ki67"),
            (patient.psa_scan, "_PSA")
        ]

        for biopsy_file, suffix in biopsy_files:
            if biopsy_file.exists():
                new_name = biopsy_file.stem + suffix + biopsy_file.suffix
                patient_biopsies_file = patient_folder / f'biopsies'
                patient_biopsies_file.mkdir(parents=True, exist_ok=True)
                destination = patient_biopsies_file / new_name

                patient.set_he_scan(destination)
                patient.set_ki67_scan(destination)
                patient.set_psa_scan(destination)

                shutil.move(str(biopsy_file), str(destination))
            else:
                print(f"File {biopsy_file} does not exist")
