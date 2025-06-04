from pathlib import Path


configfile: "config.yaml"

patients_dir = config["data_paths"]["patients"]
binary_masks_subdir = config["patient"]["binary_tissue_masks"]
patient_patches = config["patient"]["patches"]

PATIENTS = [
    p.name
    for p in Path(patients_dir).iterdir()
    if p.is_dir() and p.name.startswith("patient_")
]

rule all: 
    input:
        expand(
            f"{patients_dir}/{{patient}}/{patient_patches}",
            patient=PATIENTS
        )

rule patch_generation:
    input:
        mask = lambda wc: f"{patients_dir}/{wc.patient}/{binary_masks_subdir}/tissue_mask.png"
    output:
        patch_dir = directory(f"{patients_dir}/{{patient}}/{patient_patches}")
    params:
        pr=str(Path().absolute()),
        script = "patch_generation_smk.py",
        patient_dir = lambda wc: f"{patients_dir}/{wc.patient}"
    shell:
        r"""
        docker run --rm --entrypoint "" \
        -v "{params.pr}:/app" \
        -w "/app" \
        pc-pipeline \
        python {params.script} \
            --patient_dir "{params.patient_dir}" \
            --tissue_mask_path "{input.mask}"
        """