from pathlib import Path

configfile: "config.yaml"

patients_dir = config["data_paths"]["patients"]
biopsies_subdir = config["patient"]["biopsies"]
registered_subdir = config["patient"]["registered"]

PATIENTS = [
    p.name
    for p in Path(patients_dir).iterdir()
    if p.is_dir() and p.name.startswith("patient_")
]

rule all:
    input:
        expand(
            f"{patients_dir}/{{patient}}/{registered_subdir}",
            patient=PATIENTS
        )

rule register_biopsies:
    input:
        biopsies=lambda wc: sorted(
            str(p)
            for p in Path(f"{patients_dir}/{wc.patient}/{biopsies_subdir}").glob("*.ndpi")
        )
    output:
        registered_dir = directory(f"{patients_dir}/{{patient}}/{registered_subdir}")

    params:
        pr=str(Path().absolute()),
        script="image_registration_smk.py",
        patient_dir=lambda wc: f"{patients_dir}/{wc.patient}"
    shell:
        r"""
        docker run --rm --entrypoint "" \
          -v "{params.pr}:/app" \
          -w "/app" \
          pc-pipeline \
          python {params.script} \
            --patient_dir "{params.patient_dir}" \
            --input_files {input.biopsies}
        """
