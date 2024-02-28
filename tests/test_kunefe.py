"""Tests for the kunefe."""
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
def test_connection_with_password(monkeypatch, slurm_service):
    """Test if kunefe can ssh to the SLURM Docker container using a password."""
    responses = iter(['javagat'])  # the default password
    monkeypatch.setattr('getpass.getpass', lambda _: next(responses))
    Kunefe(username="xenon", hostname="localhost", port=10022)
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


# def test_build_apptainer_image():
#     """Test build_apptainer_image
#     """
#     pass


# def test_check_local_command_exists():
#     """Test check_local_command_exists
#     """
#     pass


def test_check_required_tools(monkeypatch):
    """Test if required tools can be found."""
    responses = iter(['javagat'])  # the default password
    monkeypatch.setattr('getpass.getpass', lambda _: next(responses))

    kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
    requirements_status = kunefe.check_required_tools(['docker', 'apptainer'])
    print(f'Requirements status: {requirements_status}')
    assert requirements_status is True, 'all the required tools need to be installed on your system'


def test_check_required_tools_fail(monkeypatch):
    """Test if check_required_tools fails for a command that does not exist."""
    responses = iter(['javagat'])  # the default password
    monkeypatch.setattr('getpass.getpass', lambda _: next(responses))

    kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
    requirements_status = kunefe.check_required_tools(['docker', 'apptainer', 'bsxcommand'])
    print(f'Requirements status: {requirements_status}')
    assert requirements_status is False, 'should fail for bsxcommand'


# def test_generate_job_file():
#     """Test generate_job_file
#     """
#     pass


# def test_run_remote_command():
#     """Test run_remote_command
#     """
#     pass


# def test_watch_slurm_queue():
#     """Test watch_slurm_queue
#     """
#     pass
