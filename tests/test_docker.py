"""Tests for the kunefe"""
from time import sleep
import docker


def test_slurm_queue():
    """Check if the SLURM service of Xenon Docker image works
    """
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

    sleep(180)
    exit_code, output = container.exec_run(
        'squeue --all',
        stderr=True,
        stdout=True
    )

    assert exit_code == 0, output

    container.stop()
    container.remove(force=True)
