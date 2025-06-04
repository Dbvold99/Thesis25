# Identifying Prostate Cancer with Deep Learning
This project uses deep learning to predict potential cancer cells in prostate cancer. For now, the preprocessing under `preprocessing` is working. Everything under `model` is not fully tested, please update this document if changes are made!

# Installation
This project requires `Docker` to be installed and running (see https://www.docker.com/).
If you want to use `Snakemake` (library for speeding up), it needs to be installed (see https://snakemake.github.io/) `TODO`: rewrite Snakemake and use it Docker. 
All other dependencies are loaded into the Docker container by `pyproject.toml`.
If you dont want to use Docker and instead run it locally on your computer please look in `pyproject.toml` under `dependencies` to see all packages required. However this might not be all packages required, because Docker uses a base image provided by VALIS (see https://valis.readthedocs.io/en/latest/installation.html).


# Running 
This step asssumes Docker is installed and running (to run Docker start `Docker Desktop`)
When running a script (expect Snakemake), please run from the `root directory` of the project. If you just did a git clone and no changes the `root directory` is `pc_pipeline`. Otherwise unexpected behaviour might happen.

## First time running
First we need to create a container, this done by typing in terminal:
`docker build -t pc-pipeline .` (Dont forget the dot and to be in the `root directory` of the project)
A container is created called `pc-pipeline`, this can take a while. When done it should be visible in `Docker Desktop`. You dont need to do this command all the time, please check Docker when it is suitable to rebuild the container.
First time please run `src.automation_scripts.init` (instructions how to run futher down) this script create necessary folders, as of now it creates two directories:
* `data/raw_scans`- Here you put all biopsies
* `data/patients` - After running `src.automation_scripts.run_associate_biopsies` patients will be created in this folder.

`DISCLAIMER:` the `model` implementation has not been fully tested. So in the `src.automation_scripts.init` you see a lot of commented lines, if you want to run the `model` you can try to remove the comments and run the scripts in `src.model.preprocess.automation_scripts` but bewere bugs may arise.
`TODO`: Fix `model` implemenatation. Honestly it might work, did an implementation but did not have time to test it. Was outside my thesis scope and time flies! I know that the files under `model/prediction` still has hard coded paths and is *not* working.


## Running a script in general
`GEEK ALERT:` I will give a short description of Docker. Docker creates a container, virtual machine, in your computer, basically a computer in your computer. The reason why this is done is because of different operating systems have different computer architecture. This means that a program that works on my computer might not work on your (classic problem). This is solved by Docker. Since Docker "creates a computer in your computer" the created computer looks the same on ALL computers, so if you have Mac/Windows/Linux it will still work. `DISCLAIMER:` The last sentence is somewhat a lie, but good enough for this. 
Since Docker is a computer in your computer when you run a script you actually make the changes on the Docker container, and not on your computer. We can solve this adding the command `docker run --rm -v "${PWD}:/app" pc-pipeline <insert script here>`. Now we basically tell our Docker "hey all changes we make in the container, aka created computer, I want those changes on my local computer as well".

When running a script (except Snakemake files) simply write following in terminal:
`docker run --rm -v "${PWD}:/app" pc-pipeline <insert script here>`
example:
`docker run --rm -v "${PWD}:/app" pc-pipeline src.automation_scripts.run_preprocess`
*Dont forget to run in root directory! This is always true*

## Running Snakemake
To run a single snakemake file please type:
`snakemake -s <file_name> --cores <amount of cores>`, ex `snakemake src/snakemake/rules/register.smk --cores 4`
*Please note `/` instead of `.`*

If you want to run all snakemake scripts just type: `bash run_all_snakemake.sh <amount of cores>`, ex `bash run_all_snakemake.sh 4`

`DISCLAIMER:` It is not best practice implementation, I was completely new to Snakemake. Currently Snakemake calls Docker. I think this should be changes so Snakemake is executed in the Docker container. It does not matter for results, only performance and being consistent.


## Running order of preprocessing
For more information about a script please open the script. Dont forget to add `docker run --rm -v "${PWD}:/app`
1. `src.automation_scripts.init`
The only thing you need to do before running remainig is to insert the biopsy scans into `data/raw_scans` folder.
2. `src.automation_scripts.run_associate_biopsies`
3. `src.automation_scripts.run_registration`
4. `src.automation_scripts.run_mask_generation`
5. `src.automation_scripts.run_patch_generation`

`OR`

Just run `src.automation_scripts.run_preprocess` (Dont forget to add the biopsy scans into `data/raw_scans` folder)

## Example of running pipeline, one step at a time
Assumes `src.automation_scripts.init` has been invoked.

1. We will insert our biopsies into the `data/raw_scans`
`raw_scans`                                                                                                                                                                                   
├── scan120.ndpi
├── scan121.ndpi
├── scan122.ndpi


2. Run `src.automation_scripts.run_associate_biopsies`
Now in `data/patients` should look the following:

.
└── patient_1
    ├── biopsies
    │   ├── scan120_HE.ndpi
    │   ├── scan121_Ki67.ndpi
    │   └── scan122_PSA.ndpi

3. Run `src.automation_scripts.run_registration`
Each patient should look like this:
.
└── patient_1
    ├── biopsies
    │   ├── scan120_HE.ndpi
    │   ├── scan121_Ki67.ndpi
    │   └── scan122_PSA.ndpi
    ├── metadata_registered
    │   ├── data
    │   │   ├── _registrar.pickle
    │   │   └── _summary.csv
    │   ├── deformation_fields
    │   │   ├── 0_scan120_HE.png
    │   │   ├── 1_scan121_Ki67.png
    │   │   └── 2_scan122_PSA.png
    │   ├── masks
    │   │   ├── _non_rigid_mask.png
    │   │   ├── scan120_HE.png
    │   │   ├── scan121_Ki67.png
    │   │   └── scan122_PSA.png
    │   ├── non_rigid_registration
    │   │   ├── 0_scan120_HE.png
    │   │   ├── 1_scan121_Ki67.png
    │   │   └── 2_scan122_PSA.png
    │   ├── overlaps
    │   │   ├── _non_rigid_overlap.png
    │   │   ├── _original_overlap.png
    │   │   └── _rigid_overlap.png
    │   ├── processed
    │   │   ├── scan120_HE.png
    │   │   ├── scan121_Ki67.png
    │   │   └── scan122_PSA.png
    │   └── rigid_registration
    │       ├── 0_scan120_HE.png
    │       ├── 1_scan121_Ki67.png
    │       └── 2_scan122_PSA.png
    └── registered
        ├── scan120_HE.ome.tiff
        ├── scan121_Ki67.ome.tiff
        └── scan122_PSA.ome.tiff


4. Run `src.automation_scripts.run_mask_generation`
Each patient now also have.
└── patient_1
    ├── binary_tissue_masks
    │   ├── blue_mask.png
    │   ├── green_mask.png
    │   ├── red_mask.png
    │   ├── tissue_mask.png
    │   └── watershed_mask.png


5. Run `src.automation_scripts.run_patch_generation` `and/or` `src.automation_scripts.run_patch_registration`
*`run_patch_generation` creates binary patches from non_rigid_overlap, meanwhile `run_patch_registration` creates patches from H&E, Ki-67 and PSA registered images*
Each patient should have folder called "Patches"





# Project Structure
Here is my project structure philosophy:
In `data` folder only have data, no code.
In `src` have all code, except `get_config.py` `TODO:` add `run_all_snakemake.sh` to `src`.

In `automation_scripts` here the scripts import modules that perform actions. These scripts could be seen as a driver 
that just performs the actions. Please see `run_registrartion.py` and `image_registration.py`. All
the code that performs registration operations are in `image_registration` and code in `run_registration` is the driver.


# Important Files
These files in this section are the bread and butter. Without them, the project wouldnt be able to run.

## Dockerfile
This file is the blueprint on how to build the container. (see https://docs.docker.com/reference/dockerfile/)

## pyproject.toml
Here we define the project, for example new dependencies is added here in the list. (see https://python-poetry.org/docs/pyproject/)

## config.yaml
All paths are defined in here, if you want a new path simply add it here. To understand how to use it check for instance `run_registration`.
Please try to avoid os.join and instead use this. In my opinion this is more readable and easier to understand.

# Known Bugs
Here are some bugs I am aware of, but did not have time to fix.

`watershed_mask.png` is currently black.
Some binary masks are not as expected. I think the error is some `morphology operation` in `mask_generation` 