from src.preprocessing.image_registration import registrar
import argparse
from pathlib import Path
from src.utils.os_lib import make_directory
from get_config import CONFIG


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--patient_dir", type=str, required=True, help="Path to patient folder")
    parser.add_argument("--input_files", type=str, nargs="+", required=True, help="List of biopsy image paths")
    parser.add_argument("--output_marker", type=str, required=False, help="Optional path to .done file for Snakemake")

    args = parser.parse_args()

    patient_path = Path(args.patient_dir)
    biopsy_files = [Path(p) for p in args.input_files]

    make_directory(patient_path, CONFIG['patient']['metadata_registered'])
    make_directory(patient_path, CONFIG['patient']['registered'])

    registrar(biopsy_files, patient_path)

    if args.output_marker:
        marker_path = Path(args.output_marker)
        marker_path.parent.mkdir(parents=True, exist_ok=True)
        marker_path.write_text("Registration complete\n")


if __name__ == '__main__':
    main()