"""An example showing how to run containerized NetLogo on HPC system."""

import os
from kunefe import Kunefe

# define the constants
USERNAME = "JaneDoe"
# folders
OUTPUT_FOLDER_LOCAL = "./output/"    # local folder to save output
REMOTE_HOME = f"/home/{USERNAME}/"   # home folder on the remote system
OUTPUT_FOLDER_REMOTE = REMOTE_HOME + "test_folder/"
# specify the Docker image
NETLOGO_VERSION = "6.3.0"
DOCKER_IMAGE = f"comses/netlogo:{NETLOGO_VERSION}"
# specify the apptainer image
SIF_FILE_NAME = f"netlogo_{NETLOGO_VERSION}.sif"
SIF_FILE_PATH_LOCAL = OUTPUT_FOLDER_LOCAL + SIF_FILE_NAME
SIF_FILE_PATH_REMOTE = OUTPUT_FOLDER_REMOTE + SIF_FILE_NAME

# We will run the NetLogo simulation on Snellius cluster:
# https://www.surf.nl/diensten/snellius-de-nationale-supercomputer
kunefe = Kunefe(username=USERNAME, hostname="snellius.surf.nl", port=22)

# create a local folder to save the generated files and the output
try:
    os.mkdir(OUTPUT_FOLDER_LOCAL)
    print(f"Directory '{OUTPUT_FOLDER_LOCAL}' created.")
except FileExistsError:
    print(f"Directory '{OUTPUT_FOLDER_LOCAL}' already exists.")

# build apptainer image from a Docker image
kunefe.build_apptainer_image(
    docker_image=DOCKER_IMAGE, sif_file_name=SIF_FILE_PATH_LOCAL
)

# make a connection to the remote
kunefe.connect_remote()

# create a folder which the files will be copied to
kunefe.create_remote_folder(remote_folder=OUTPUT_FOLDER_REMOTE)

# define the job name and the command to be used to run NetLogo
JOB_NAME = "kunefe_netlogo_experiment_job"
NETLOGO_COMMAND = """/opt/netlogo/netlogo-headless.sh \
--model 'model_path' \
--experiment 'experiment_name' \
--table 'table_name'
"""

# generate a job script to be submitted to HPC job queue
kunefe.generate_job_script(
    job_name=JOB_NAME,
    sif_file_path=SIF_FILE_PATH_REMOTE,
    command=NETLOGO_COMMAND,
    env_vars="JAVA_TOOL_OPTIONS=-Xmx8G",
    job_file_path=OUTPUT_FOLDER_LOCAL,
    job_time="0:1:00",
    template_name="generic",
)

# copy the required files and the job script to the remote system
kunefe.put_files(remote_folder=OUTPUT_FOLDER_REMOTE, local_folder=OUTPUT_FOLDER_LOCAL, verbose=True)

# submit the job
job_id, stdin, stdout, stderr = kunefe.submit_job(
    job_file=f"{OUTPUT_FOLDER_REMOTE}/{JOB_NAME}.sh"
)

# monitor the queue
kunefe.watch_slurm_queue()

# the method below can be used to retrieve the job results
# kunefe.get_files(remote_folder=OUTPUT_FOLDER_REMOTE, local_folder=f"{OUTPUT_FOLDER_LOCAL}/result")
