"""A complete example showing how to test kunefe module."""

import os
from kunefe import Kunefe

# set up a local slurm cluster
# docker pull xenonmiddleware/slurm:latest
# docker run --detach --publish 10022:22 xenonmiddleware/slurm:latest

## generate an apptainer image
# initialize kunefe by providing connection details

# run using xenon
# kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
# home_folder = "/home/xenon/"

# run on snellius
kunefe = Kunefe(username="olyashevska", hostname="snellius.surf.nl", port=22)
home_folder = "/home/olyashevska/"

# create test folder
local_folder = "./test_folder/"
try:
    os.mkdir(local_folder)
    print(f"Directory '{local_folder}' created.")
except FileExistsError:
    print(f"Directory '{local_folder}' already exists.")

# specify the Docker image to use
version = "6.3.0"
docker_image = f"comses/netlogo:{version}"
sif_file_name = "netlogo_6.3.0.sif"
local_sif_file_path = local_folder + sif_file_name

remote_folder = home_folder + "test_folder/"
remote_sif_file_path = remote_folder + sif_file_name

# build apptainer image from a Docker image
kunefe.build_apptainer_image(
    docker_image=docker_image, sif_file_name=local_sif_file_path
)

kunefe.connect_remote()

kunefe.create_remote_folder(remote_folder=remote_folder)

## generate a job script
netlogo_command = """/opt/netlogo/netlogo-headless.sh \
--model 'model_path' \
--experiment 'experiment_name' \
--table 'table_name'
"""

kunefe.generate_job_script(
    job_name="kunefe_netlogo_experiment_job",
    sif_file_path=remote_sif_file_path,
    command=netlogo_command,
    env_vars="JAVA_TOOL_OPTIONS=-Xmx8G",
    job_file_path=local_folder,
    job_time="0:1:00",
    template_name="generic",
)

## copy the required files and the job script to the remote system

kunefe.put_files(remote_folder=remote_folder, local_folder=local_folder, verbose=True)

## submit the job
# job_id, stdin, stdout, stderr = kunefe.submit_job(job_file="/home/xenon/test_folder/kunefe_netlogo_experiment_job.sh")
job_id, stdin, stdout, stderr = kunefe.submit_job(
    job_file="/home/olyashevska/test_folder/kunefe_netlogo_experiment_job.sh"
)

## monitor the queue
kunefe.watch_slurm_queue()

## retrive the job results
# kunefe.get_files(remote_folder=remote_folder, local_folder="./copy_of_test_folder")
