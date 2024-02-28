"""Tests for the kunefe"""
from time import sleep
import pytest
import docker
from kunefe import Kunefe


# To see the print messages run with '--capture=no':
# pytest --capture=no -v tests/test_kunefe.py
@pytest.fixture(scope='session', autouse=True)
def slurm_service():
    """Start the SLURM service before running the tests
    """
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
    """Test if kunefe can ssh to the SLURM Docker container using a password
    """
    responses = iter(['javagat'])  # the default password
    monkeypatch.setattr('getpass.getpass', lambda _: next(responses))
    Kunefe(username="xenon", hostname="localhost", port=10022)
    # assert Kunefe(username="xenon", hostname="localhost", port=10022) == ("Me", "xxx")
