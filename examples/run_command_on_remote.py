from kunefe import Kunefe

# initialize kunefe by providing connection details
kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)

# set up clients and connect to the remote
kunefe.connect_remote()

# run 'ls' command on the remote system and show the output
stdin, stdout, stderr = kunefe.run_remote_command(command='ls /home/xenon')
print(f'stdin:\n{stdin}')
print(f'stdout:\n{stdout}')
print(f'stderr:\n{stderr}')

# run 'ls' command for non-existent path
stdin, stdout, stderr = kunefe.run_remote_command(command='ls /home/sweet/home')
print(f'stdin:\n{stdin}')
print(f'stdout:\n{stdout}')
print(f'stderr:\n{stderr}')

# # run 'ls'but clean the output
# kunefe.run_remote_command(command='ls -la', flush=True)
