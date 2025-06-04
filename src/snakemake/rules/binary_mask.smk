from pathlib import Path

configfile: "config.yaml"

patients_dir = config["data_paths"]["patients"]
overlap_subpath = config["patient"]["non_rigid_overlap_biopsy"]
binary_masks_subdir = config["patient"]["binary_tissue_masks"]

PATIENTS = [
    p.name
    for p in Path(patients_dir).iterdir()
    if p.is_dir() and p.name.startswith("patient_")
]

rule all:
    input:
        expand(
            f"{patients_dir}/{{patient}}/{binary_masks_subdir}",
            patient=PATIENTS
        )

rule mask_binary:
    input:
        overlap=lambda wc: f"{patients_dir}/{wc.patient}/{overlap_subpath}"
    output:
        masks_dir=directory(f"{patients_dir}/{{patient}}/{binary_masks_subdir}")
    params:
        pr=str(Path().absolute()),
        script="mask_binary_smk.py",
        patient_dir=lambda wc: f"{patients_dir}/{wc.patient}"
    shell:
        r"""
        docker run --rm --entrypoint "" \
          -v "{params.pr}:/app" \
          -w "/app" \
          pc-pipeline \
          python {params.script} \
            --patient_dir "{params.patient_dir}" \
            --registration {input.overlap}
        """