'''
This submodule is for processing files.

Following functions exists:

count_subfolders(folder:str) -> int
    Iterates through current folder and count every folder directy under it (sub-subfolders are not accounted for)

get_subfolders(folder:str) -> List[Path]
    Iterates through current folder and returns every top-level subfolder

get_files_in_folder(folder: str, file_type: Optional[str] = None) -> List[Path]
    Iterates through a folder and collects all files, you can give a specific file type, e.g. .png.

numerically_sort_files_in_folder(folder:str) -> List[Path]:
    sorts the files, this is usually done automatically by the computer. But since it is very important, 
    when creating a patient we iterate through 'raw_scans' in ascending order, it is a safegaurd.

get_numbers(path_or_string: Union[str, List[int]]) -> List[int]:
    Uses Regular expression to get all the numbers from a string
    Example: foo3333bar -> 3333

'''



from typing import List, Optional, Union
from pathlib import Path
import re

def count_subfolders(folder:str) -> int:
    '''
    Counts the number of subfolders directly under parent.
    '''

    folder = Path(folder)
    return sum(1 for subfolder in folder.iterdir() if subfolder.is_dir())

def get_subfolders(folder:str) -> List[Path]:
    '''
    returns all top-level subfolders in current folder
    '''
    current_folder = Path(folder)

    return [sub_folder for sub_folder in current_folder.iterdir() if sub_folder.is_dir()]

def get_files_in_folder(folder: str, file_type: Optional[str] = None) -> List[Path]:
    '''
    Collects all files in a folder.
    If file_type is specified, only files with that extension are returned.
    '''
    folder_path = Path(folder)
    if file_type:
        return list(folder_path.glob(f'*.{file_type}'))
    else:
        return [f for f in folder_path.iterdir() if f.is_file()]
    
def get_files_from_specific_folder(current_folder: str, specified_folder:str):
    '''
    Finds the specified folder and returns all files in folder.
    '''
    folder_path = Path(current_folder) / specified_folder
    return [f for f in folder_path.iterdir() if f.is_file()]

def make_directory(current_folder: Path, new_folder:str):
    '''
    Creates a directory in current_folder
    '''
    path = current_folder / new_folder
    path.mkdir(parents=True, exist_ok=True)

def get_absolute_paths(files_in_folder: List[Path]) -> List[Path]:
    '''
    Gets the absolute_path
    '''
    return [path.resolve() for path in files_in_folder]


def numerically_sort_files_in_folder(folder:str) -> List[Path]:
    '''
    sorts the files in folder in ascending order
    '''
    return sorted(get_files_in_folder(folder), key=lambda f: get_numbers(f.name))


def get_numbers(path_or_string: Union[str, List[int]]) -> List[int]:
    '''
    Returns all numbers found in a string or in a PosixPath.
    '''
    string = str(path_or_string)
    return [int(num) for num in re.findall(r'\d+', string)]
