#!/bin/bash
#SBATCH -N 1
#SBATCH -c 1
#SBATCH --mem=64G
#SBATCH -t 60:00:00 
#SBATCH -J strabospot_clustering
#SBATCH -o slurm-%j.out
#SBATCH -p intel


echo "Job ${SLURM_JOB_ID} started on ${HOSTNAME} at $(date)"
echo "========================================"

# Loads environment
module load anaconda3
source activate jupyter_env

pip install -r ../requirements.txt

# Runs first Python script
echo "Running clustering.py..."
echo "Started at $(date)"
python -u clustering.py

if [ $? -eq 0 ]; then
    echo "clustering.py completed successfully at $(date)"
else
    echo "clustering.py FAILED"
    exit 1
fi

echo ""
echo "========================================"
echo ""

# Runs second Python script
echo "Running clustering_analysis.py..."
echo "Started at $(date)"
python -u clustering_analysis.py

if [ $? -eq 0 ]; then
    echo "clustering_analysis.py completed successfully at $(date)"
else
    echo "clustering_analysis.py FAILED"
    exit 1
fi

echo ""
echo "========================================"
echo "Job completed at $(date)"

