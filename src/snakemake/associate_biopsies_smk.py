import argparse
from pathlib import Path
from src.preprocessing.associate_biopsies import associate_biopsies


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, required=True, help="Dummy output to signal done")
    args = parser.parse_args()

    associate_biopsies()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("biopsies associated\n")

if __name__ == '__main__':
    main()