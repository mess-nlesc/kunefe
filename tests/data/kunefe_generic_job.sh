
#!/bin/bash
#SBATCH --job-name pytest_job
#SBATCH --output pytest_job.out
#SBATCH --error pytest_job.err
#SBATCH --time 0:30:00
#SBATCH --mem=8GB
#SBATCH --ntasks 1

apptainer exec --env "PATH=$PATH:/home/xenon" \
    /home/xenon/myapp_0.1.0.sif ls /home/xenon
