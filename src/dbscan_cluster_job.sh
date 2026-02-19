#!/bin/bash
#SBATCH -N 1
#SBATCH -c 1
#SBATCH --mem=128G
#SBATCH -t 60:00:00 
#SBATCH -J strabospot_clustering
#SBATCH -o slurm-%j.out
#SBATCH -p intel


echo "Job ${SLURM_JOB_ID} started on ${HOSTNAME} at $(date)"
echo "========================================"

pip install -r ../requirements.txt

echo "Running dbscan_clustering.py..."
echo "Started at $(date)"
python -u dbscan_clustering.py

if [ $? -eq 0 ]; then
    echo "clustering.py completed successfully at $(date)"
else
    echo "clustering.py FAILED"
    exit 1
fi

echo ""
echo "========================================"
echo "Job completed at $(date)"

