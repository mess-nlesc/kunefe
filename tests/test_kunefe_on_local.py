"""Tests local functions of kunefe."""
import os
import pytest
from kunefe import Kunefe

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"

@pytest.fixture
def generic_job_sample_file():
    """Test Employee Fixture."""
    with open("tests/data/kunefe_generic_job.sh", mode="r", encoding="utf-8") as file:
        data = file.read().rstrip()
        return data


#@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping the test: Test does not work in Github Actions.")
def test_build_apptainer_image(tmp_path):
    """Test build_apptainer_image."""
    print(f'\nworkdir: {tmp_path}')
    kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
    assert kunefe.build_apptainer_image(
        docker_image='comses/netlogo:6.3.0',
        sif_file_name=f'{tmp_path}/netlogo_6.3.0.sif'
    )


#@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping the test: Test does not work in Github Actions.")
def test_build_apptainer_image_fail(tmp_path):
    """Test build_apptainer_image."""
    print(f'\nworkdir: {tmp_path}')
    kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
    assert not kunefe.build_apptainer_image(
        docker_image='someorg/someimage:99.99.0',
        sif_file_name=f'{tmp_path}/someimage_99.99.0.sif'
    )


# # See https://stackoverflow.com/a/52877169
# def test_compare_generated_apptainer_image():
#     """Test build_apptainer_image
#     """
#     pass


def test_check_local_command_exists():
    """Test check_local_command_exists."""
    kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
    assert kunefe.check_local_command_exists(command='ls')


def test_check_local_command_exists_fail():
    """Test check_local_command_exists."""
    kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
    assert not kunefe.check_local_command_exists(command='thisdoesnotexist')


# to only test this function run:
# pytest --capture=no -v tests/test_kunefe.py::test_check_required_tools
def test_check_required_tools():
    """Test if required tools can be found."""
    kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
    requirements_status = kunefe.check_required_tools(['docker', 'rsync'])
    print(f'Requirements status: {requirements_status}')
    assert requirements_status is True, 'all the required tools need to be installed on your system'


# to only test this function run:
# pytest --capture=no -v tests/test_kunefe.py::test_check_required_tools_fail
def test_check_required_tools_fail():
    """Test if check_required_tools fails for a command that does not exist."""
    kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
    requirements_status = kunefe.check_required_tools(['docker', 'rsync', 'bsxcommand'])
    print(f'Requirements status: {requirements_status}')
    assert requirements_status is False, 'should fail for bsxcommand'


# https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html
def test_generate_job_script(tmp_path, generic_job_sample_file):
    """Test generate_job_script."""
    print(f'\nworkdir: {tmp_path}')
    # print(generic_job_sample_file)

    kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
    kunefe.generate_job_script(
        job_name='pytest_job',
        sif_file_path="/home/xenon/myapp_0.1.0.sif",
        command="ls /home/xenon",
        env_vars="PATH=$PATH:/home/xenon",
        job_time='0:30:00',
        job_file_path=tmp_path
    )

    generated_file_content = None
    generated_file_path = f"{tmp_path}/pytest_job.sh"
    with open(generated_file_path, mode="r", encoding="utf-8") as file:
        generated_file_content = file.read().rstrip()
    # print(generated_file_content)

    assert generic_job_sample_file == generated_file_content
