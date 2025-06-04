import subprocess
import time
import sys

def run_snakemake_workflows(cores=1):
    snakefiles = [
        "src/snakemake/rules/register.smk",
        "src/snakemake/rules/binary_mask.smk",
        "src/snakemake/rules/patch_gen.smk"
    ]

    for sf in snakefiles:
        print("————————————————————————————")
        print(f"Running workflow: {sf} (using {cores} cores)")
        start = time.time()
        try:
            subprocess.run(
                ["snakemake", "-s", sf, "--cores", str(cores)],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error: Snakemake failed on {sf}")
            sys.exit(e.returncode)
        end = time.time()
        elapsed = end - start
        minutes, seconds = divmod(int(elapsed), 60)
        print(f"{sf} took {minutes}m{seconds}s")

    print("All done!")

if __name__ == "__main__":

    cores = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    run_snakemake_workflows(cores)
