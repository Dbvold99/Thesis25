from pathlib import Path

class Patient:
    '''
    A patient has an ID and the paths to their biopsies scan
    #TODO: add meta data, so we can rebuild images from patches
    '''

    def __init__(self, id: int, he_scan: Path, ki67_scan: Path, psa_scan: Path):
        self.id = id
        self.he_scan = he_scan
        self.ki67_scan = ki67_scan
        self.psa_scan = psa_scan

    def __str__(self):
        return f'{self.id} \n {self.he_scan} \n {self.ki67_scan} \n {self.psa_scan}'
    
    def get_id(self):
        return self.id

    def get_he_scan(self):
        return self.he_scan
    
    def get_ki67_scan(self):
        return self.ki67_scan
    
    def get_psa_scan(self):
        return self.psa_scan
    
    def set_he_scan(self, new_path: Path):
        self.he_scan = new_path

    def set_ki67_scan(self, new_path: Path):
        self.ki67_scan = new_path

    def set_psa_scan(self, new_path: Path):
        self.psa_scan = new_path