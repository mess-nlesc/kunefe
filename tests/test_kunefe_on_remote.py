"""Tests remote functions of kunefe ."""
from time import sleep
import docker
import pytest
from kunefe import Kunefe


# To see the print messages run with '--capture=no':
# pytest --capture=no -v tests/test_kunefe.py
@pytest.fixture(scope='session', autouse=True)
def slurm_service():
    """Start the SLURM service before running the tests."""
    container_name = "test_kunefe_remote"
    docker_image_name = "nlesc/kunefe:slurm"

    # https://docker-py.readthedocs.io/en/stable/containers.html
    # start the SLURM service before tests
    client = docker.from_env()
    print(f'\nStarting the Docker container using image: {docker_image_name}')
    container = client.containers.run(
        name=container_name,
        image=docker_image_name,
        detach=True,
        ports={'22/tcp': 10022}
    )

    wait_time_container_start = 10
    wait_time_slurm_service = 240

    print(f'Waiting {wait_time_container_start} seconds for container to start')
    sleep(wait_time_container_start)  # wait 10 sec for container to start

    container_state = container.attrs['State']
    assert container_state['Status'] == 'created'

    print(f'Waiting {wait_time_slurm_service} seconds for SLURM service to start')
    for seconds in range(wait_time_slurm_service, 0, -1):
        print(f"{seconds} seconds left  ", end="\r", flush=True)
        sleep(1)

    yield container

    # stop the SLURM service and remove the container after the last test
    print('\nStopping and removing the Docker container')
    container.stop()
    container.remove(force=True)


# https://docs.pytest.org/en/latest/how-to/monkeypatch.html
# to only test this function run:
# pytest --capture=no -v tests/test_kunefe.py::test_connection_with_password
def test_connection_with_password(monkeypatch, slurm_service):
    """Test if kunefe can ssh to the SLURM Docker container using a password."""
    responses = iter(['javagat'])  # the default password
    monkeypatch.setattr('getpass.getpass', lambda _: next(responses))
    kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
    kunefe.connect_remote()
    # assert Kunefe(username="xenon", hostname="localhost", port=10022) == ("Me", "xxx")


# def test_create_remote_folder():
#     """Test if a remote folder is created successfully
#     """
#     pass


# def test_get_files():
#     """Test get_files
#     """
#     pass


# def test_put_files():
#     """Test put_files
#     """
#     pass


def test_submit_job(monkeypatch, slurm_service):
    """Test if a job is submitted successfully."""
    responses = iter(['javagat'])  # the default password
    monkeypatch.setattr('getpass.getpass', lambda _: next(responses))
    kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
    kunefe.connect_remote()
    job_id, stdin, stdout, stderr = kunefe.submit_job(
        job_file="/home/xenon/test-slurm.job"
    )
    print(f'job_id: {job_id}')
    assert stderr == '', 'there was an error'


def test_run_remote_command(monkeypatch, slurm_service):
    """Test if a command runs succesfully on the remote system."""
    responses = iter(['javagat'])  # the default password
    monkeypatch.setattr('getpass.getpass', lambda _: next(responses))
    kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
    kunefe.connect_remote()
    _, stdout, stderr = kunefe.run_remote_command(command='ls /home/xenon')
    assert stderr == '', 'there was an error'
    assert stdout == 'filesystem-test-fixture\ntest-slurm.job\n', 'the command output does not match'



# def test_watch_slurm_queue():
#     """Test watch_slurm_queue
#     """
#     pass
