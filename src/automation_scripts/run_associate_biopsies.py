'''
This script moves biopsies from 'data/raw_scans' to 'patient' folder and create a subfolder for each patient with their biopsies
'''
from src.preprocessing.associate_biopsies import associate_biopsies

def run_associate_biopsies():
    associate_biopsies()

if __name__ == '__main__':
    run_associate_biopsies()