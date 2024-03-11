#!/usr/bin/env python
"""A script to test kunefe module."""

from kunefe import Kunefe

kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)

# set up the clients and connect to the remote
# kunefe.connect_remote()

# # submit a new job
# job_id, stdin, stdout, stderr = kunefe.submit_job(
#     job_file="/home/xenon/test-slurm.job"
# )
# print(f'job_id: {job_id}')

# # copy files to the server
# kunefe.put_files(
#     remote_folder="/home/xenon/",
#     local_folder="./test_folder"
# )

# # download files from the server
# kunefe.get_files(
#     remote_folder="/home/xenon/test_folder",
#     local_folder="./copy_of_test_folder"
# )

# # check if the required tools (commands) available on the host system
# requirements_status = kunefe.check_required_tools(['docker', 'apptainer'])
# print(f'Requirements status: {requirements_status}')

# # build the apptainer image from the docker image
# image_build_status = kunefe.build_apptainer_image(netlogo_version='6.3.0')
# print(f'Image build status: {image_build_status}')

# # watch the slurm queue
# kunefe.watch_slurm_queue()
