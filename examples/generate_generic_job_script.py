from kunefe import Kunefe

# initialize kunefe by providing connection details
kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)

# generate a slurm job script
kunefe.generate_job_script(
    job_name='kunefe_generic_job',
    sif_file_path="/home/xenon/myapp_0.1.0.sif",
    command="ls /home/xenon",
    env_vars="PATH=$PATH:/home/xenon",
    job_time='0:30:00',
)
