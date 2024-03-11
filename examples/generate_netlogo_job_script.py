from kunefe import Kunefe

# initialize kunefe by providing connection details
kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)

# netlogo command to run simulation in headless mode
netlogo_command = """/opt/netlogo/netlogo-headless.sh \
--model 'model_path' \
--experiment 'experiment_name' \
--table 'table_name'
"""

# generate a slurm job script
kunefe.generate_job_script(
    job_name='kunefe_netlogo_experiment_job',
    sif_file_path="/home/xenon/netlogo_6.3.0.sif",
    command=netlogo_command,
    env_vars="JAVA_TOOL_OPTIONS=-Xmx8G",
    job_time='0:30:00',
    template_name='generic'
)
