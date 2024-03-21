from kunefe import Kunefe

# initialize kunefe by providing connection details
kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)

# set up clients and connect to the remote
kunefe.connect_remote()

kunefe.install_apptainer_on_remote(install_path="/home/xenon/tools/")
