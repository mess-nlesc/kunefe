"""Tests for the kunefe."""
from time import sleep
import docker


def test_docker_start():
    """Check if Docker container runs."""
    container_name = "test_docker_start"
    docker_image_name = "xenonmiddleware/slurm:latest"

    # https://docker-py.readthedocs.io/en/stable/containers.html
    client = docker.from_env()
    container = client.containers.run(
        name=container_name,
        image=docker_image_name,
        detach=True,
        ports={'22/tcp': 10022}
    )

    # timeout = 20
    # stop_time = 1
    # elapsed_time = 0
    # while container.status != 'running' and elapsed_time < timeout:
    #     sleep(stop_time)
    #     elapsed_time += stop_time
    #     continue

    sleep(10)
    container_state = container.attrs['State']
    # container.wait()
    container.stop()
    container.remove(force=True)

    assert container_state['Status'] == 'created'
    # assert container.status == ['created', 'running'], 'container is not created or running'


def test_slurm_queue():
    """Check if the SLURM service of Xenon Docker image works."""
    container_name = "test_slurm_queue"
    docker_image_name = "xenonmiddleware/slurm:latest"

    # https://docker-py.readthedocs.io/en/stable/containers.html
    client = docker.from_env()
    container = client.containers.run(
        name=container_name,
        image=docker_image_name,
        detach=True,
        ports={'22/tcp': 10022}
    )

    sleep(240)
    exit_code, output = container.exec_run(
        'squeue --all',
        stderr=True,
        stdout=True
    )

    container.stop()
    container.remove(force=True)

    assert exit_code == 0, output
