"""A complete example to test kunefe module."""

from kunefe import Kunefe

## generate an apptainer image
# initialize kunefe by providing connection details
kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)

netlogo_version = "6.3.0"
netlogo_docker_image = f"comses/netlogo:{netlogo_version}"
netlogo_sif_file_name = "netlogo_6.3.0.sif"

# build apptainer image from a Docker image
kunefe.build_apptainer_image(docker_image=netlogo_docker_image, sif_file_name=netlogo_sif_file_name)

## generate a job script
# netlogo command to run simulation in headless mode
netlogo_command = """/opt/netlogo/netlogo-headless.sh \
--model 'model_path' \
--experiment 'experiment_name' \
--table 'table_name'
"""

# generate a slurm job script
kunefe.generate_job_script(
    job_name="kunefe_netlogo_experiment_job",
    sif_file_path="/home/xenon/netlogo_6.3.0.sif",
    command=netlogo_command,
    env_vars="JAVA_TOOL_OPTIONS=-Xmx8G",
    job_time="0:30:00",
    template_name="generic",
)

## copy the required files and the job script to the remote system

# # copy files to the server
# kunefe.put_files(
#     remote_folder="/home/xenon/",
#     local_folder="./test_folder"
# )

## submit the job
# kunefe.connect_remote()

# # submit a new job
# job_id, stdin, stdout, stderr = kunefe.submit_job(
#     job_file="/home/xenon/test-slurm.job"
# )

## monitor the queue
# kunefe.watch_slurm_queue()

## retrive the job results

# kunefe.get_files(
#     remote_folder="/home/xenon/test_folder",
#     local_folder="./copy_of_test_folder"
# )