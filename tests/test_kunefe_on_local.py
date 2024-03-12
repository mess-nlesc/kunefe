"""Tests local functions of kunefe."""
from kunefe import Kunefe


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
