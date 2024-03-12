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
    container_name = "test_kunefe"
    docker_image_name = "xenonmiddleware/slurm:latest"

    # https://docker-py.readthedocs.io/en/stable/containers.html
    # start the SLURM service before tests
    client = docker.from_env()
    print('\nStarting the Docker container')
    container = client.containers.run(
        name=container_name,
        image=docker_image_name,
        detach=True,
        ports={'22/tcp': 10022}
    )
    sleep(10)
    container_state = container.attrs['State']
    assert container_state['Status'] == 'created'

    yield container

    # stop the SLURM service after the last test
    print('\nStopping the Docker container')
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
#     """Test create_remote_folder
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


# def test_submit_job():
#     """Test submit_job
#     """
#     pass


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
