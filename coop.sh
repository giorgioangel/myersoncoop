#!/bin/bash

#SBATCH --job-name=coop2
#SBATCH --partition=short
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --begin=now
#SBATCH --mail-user=giorgio.angelotti@isae.fr
#SBATCH --mail-type=BEGIN,FAIL,END

module load python/3.8
source activate dsym-gpu
export LD_LIBRARY_PATH=/home/dcas/g.angelotti/.conda/envs/dsym-gpu/lib:$LD_LIBRARY_PATH

python -W ignore main.py --exact 5 --mc_num 10000 --sim_num 300
