"""Tests local functions of kunefe."""
from kunefe import Kunefe


def test_build_apptainer_image(tmp_path):
    """Test build_apptainer_image."""
    print(f'\nworkdir: {tmp_path}')
    kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
    assert kunefe.build_apptainer_image(
        docker_image='comses/netlogo:6.3.0',
        sif_file_name=f'{tmp_path}/netlogo_6.3.0.sif'
    )


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
