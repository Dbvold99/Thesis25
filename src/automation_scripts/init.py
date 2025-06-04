"""
This module sets-up the project, creating necessary folders. This script is automatically runned when creating a Docker container. If not using Docker please run this script.
"""
from get_config import CONFIG
from src.utils.os_lib import make_directory
from pathlib import Path

def init():
    patients = CONFIG["data_paths"]["patients"]
    raw_scans = CONFIG["data_paths"]["raw_scans"]
    #training = CONFIG["data_paths"]["training"]
    #tumor_scans = CONFIG["data_paths"]["tumor_annotations"]
    #cell_scans = CONFIG["data_paths"]["cell_annotations"]
    #training_data = CONFIG["data_paths"]["training_data"]
    root_folder = Path().absolute()

    print(f"Creating folders: {patients}, {raw_scans}")
    make_directory(root_folder, patients)
    make_directory(root_folder, raw_scans)
    #make_directory(root_folder, training)
    #make_directory(root_folder, tumor_scans)
    #make_directory(root_folder, cell_scans)
    #make_directory(root_folder, training_data)
    print(f"DONE creating: {patients}, {raw_scans}")


if __name__ == '__main__':
    init()