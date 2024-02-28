from kunefe import Kunefe

# initialize kunefe by providing connection details
kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)

# run 'ls' command on the remote system
kunefe.run_remote_command(command='ls /home/xenon')

# # run 'ls'but clean the output
# kunefe.run_remote_command(command='ls -la', flush=True)
