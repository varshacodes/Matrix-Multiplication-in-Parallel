
#!/bin/sh
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute
#SBATCH --time=01:30:00
#SBATCH --nodes=32
#SBATCH --ntasks-per-node=1
#SBATCH --mem=3000
#SBATCH --job-name="test"
#SBATCH --output=test-%j.out
#SBATCH --mail-user=vganesh2@buffalo.edu
#SBATCH --mail-type=END
#SBATCH --constraint=IB&CPU-E5645
#SBATCH --exclusive
echo "SLURM_JOBID="$SLURM_JOBID
echo "SLURM_JOB_NODELIST="$SLURM_JOB_NODELIST
echo "SLURM_NNODES="$SLURM_NNODES
echo "SLURMTMPDIR="$SLURMTMPDIR
echo "working directory = "$SLURM_SUBMIT_DIR
ulimit -s unlimited
module load mpi4py
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so
module list
which python
echo "Launch job"
python generateData.py 32 100
srun -n 32 python matrix.py 32 100
echo "All Done!"