'''
Runs the entire preprocess pipeline
'''
from src.automation_scripts.run_associate_biopsies import run_associate_biopsies
from src.automation_scripts.run_registration import run_registration
from src.automation_scripts.run_mask_generation import run_mask_generation
from src.automation_scripts.run_patch_generation import run_patch_generation


def run_preprocess():
    run_associate_biopsies()
    run_registration()
    run_mask_generation()
    run_patch_generation()


if __name__ == '__main__':
    run_preprocess()