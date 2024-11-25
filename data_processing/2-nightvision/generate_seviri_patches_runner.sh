#!/bin/bash
#SBATCH --partition="short-serial-4hr"
#SBATCH --account=short4hr
#SBATCH --time=0:15:00
#SBATCH --mem=16000
#SBATCH --job-name=seviri_patch
#SBATCH -o ./log_files/%A_%a.out
#SBATCH -e ./log_files/%A_%a.err
#SBATCH --array=0-364
START_DATE="2019-01-01"
./generate_seviri_patches.py $(date +%Y-%m-%d -d "${START_DATE} + ${SLURM_ARRAY_TASK_ID} day")
