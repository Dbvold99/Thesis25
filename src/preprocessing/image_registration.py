'''
This modules takes the biopsies from each patient and registers them together. It creates following subfolders in patient_*:
    metadata_registered: Containing different outputs from Valis. The output we are mostly interested in is in folder metadata_registered/overlaps,
    here the biopsies are aligned.
    registered: the biopsies converted from .ndpi to ome.tiff 
'''

from valis import registration
from typing import List
from pathlib import Path
from get_config import CONFIG


def registrar(path_patient_biopsies: List[Path], absolute_path_patient: Path):

    try: 
        registrar = registration.Valis(
            "",
            str(absolute_path_patient / CONFIG['patient']['metadata_registered']),
            img_list=[str(p) for p in path_patient_biopsies],
            max_processed_image_dim_px=1024,
            imgs_ordered=True
        )

        rigid_registrar, non_rigid_registrar, error_df = registrar.register()

        registrar.warp_and_save_slides(
            str(absolute_path_patient / CONFIG['patient']['registered']),
            compression="lzw"
        )

    except Exception as e:
        print(f'Error details: {str(e)}')

    finally:
        registration.kill_jvm()