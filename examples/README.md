<!-- examples/README.md -->
<!-- Run: python -m doctest -v examples/README.md -->

# Kunefe examples

The `kunefe` Python module provides functions to run docker images on HPC systems.

Here are a few examples of how to use the functions in `kunefe`:

## initialization

```python
>>> from kunefe import Kunefe
>>> kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)

```

## Check if a command exists on the host machine

```python
>>> kunefe.check_local_command_exists(command='ls')
True
>>> kunefe.check_local_command_exists(command='thisdoesnotexist')
False

```

## Check required tools to run the package

```python
>>> kunefe.check_required_tools(['ls', 'rsync', 'cp'])
True

>>> kunefe.check_required_tools(['docker', 'rsync', 'bsxcommand'])
False

```

## Extra: Run a shell command

```python
>>> import subprocess
>>> run_command = lambda cmd: subprocess.check_output(cmd, shell=True).decode().strip()

```

```python
>>> print(run_command("date +'%Y'"))
2024

```

## build an image

```python
# remove existing the sif if it exists
>>> run_command('rm -f netlogo_6.3.0.sif')
''

# define the docker image
>>> netlogo_version = "6.3.0"
>>> netlogo_docker_image = f"comses/netlogo:{netlogo_version}"
>>> netlogo_sif_file_name = "netlogo_6.3.0.sif"

# build apptainer image from a Docker image
>>> kunefe.build_apptainer_image(docker_image=netlogo_docker_image, sif_file_name=netlogo_sif_file_name)
Generated netlogo_6.3.0.sif
True

# clean up
>>> run_command('rm -f netlogo_6.3.0.sif')
''

```

## generate a job script

```python
# generate a slurm job script
>>> kunefe.generate_job_script(job_name='kunefe_generic_job', sif_file_path="/home/xenon/myapp_0.1.0.sif", command="ls /home/xenon", env_vars="PATH=$PATH:/home/xenon", job_time='0:30:00')
Batch job file was saved as .//kunefe_generic_job.sh

# clean up
>>> run_command('rm -f kunefe_generic_job.sh')
''

```

## generate a NetLogo job script

```python
# netlogo command to run simulation in headless mode
>>> netlogo_command = "/opt/netlogo/netlogo-headless.sh --model 'model_path' --experiment 'experiment_name' --table 'table_name'"

>>> kunefe.generate_job_script(job_name='kunefe_netlogo_experiment_job', sif_file_path="/home/xenon/netlogo_6.3.0.sif", command=netlogo_command, env_vars="JAVA_TOOL_OPTIONS=-Xmx8G", job_time='0:30:00', template_name='generic')
Batch job file was saved as .//kunefe_netlogo_experiment_job.sh

# clean up
>>> run_command('rm -f kunefe_netlogo_experiment_job.sh')
''

```

## running a command on the remote system

```python
# set up clients and connect to the remote
>> kunefe.connect_remote()

# run 'ls' command on the remote system and show the output
>> stdin, stdout, stderr = kunefe.run_remote_command(command='ls /home/xenon')
>> print(f'stdin:\n{stdin}')
>> print(f'stdout:\n{stdout}')
>> print(f'stderr:\n{stderr}')

```

## installing Apptainer on the remote system

```python
# set up clients and connect to the remote
>> kunefe.connect_remote()

# install apptainer to `/home/xenon/tools` on the remote system
>> kunefe.install_apptainer_on_remote(install_path="/home/xenon/tools")

```

## submit a job using existing job script

```python
# set up clients and connect to the remote
>> kunefe.connect_remote()

# submit a new job
>> job_id, stdin, stdout, stderr = kunefe.submit_job(
>>     job_file="/home/xenon/test-slurm.job"
>> )
>> print(f'job_id: {job_id}')

```

## copy files from the remote system

```python
# set up clients and connect to the remote
>> kunefe.connect_remote()

# download files from the server
>> kunefe.get_files(
>>     remote_folder="/home/xenon/test_folder",
>>     local_folder="./copy_of_test_folder"
>> )

```

## copy files to the remote system

```python
# set up clients and connect to the remote
>> kunefe.connect_remote()

# copy files to the server
>> kunefe.put_files(
>>     remote_folder="/home/xenon/",
>>     local_folder="./test_folder"
>> )

```

## A complete example

A complete example can be found at [complete_example.py](complete_example.py)


<!-- ## Title

```python
>>>
``` -->
