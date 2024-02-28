"""Tests for the kunefe"""
from kunefe import Kunefe

# https://docs.pytest.org/en/latest/how-to/monkeypatch.html
def test_connection_with_password(monkeypatch):
    """Test if kunefe can ssh to the SLURM Docker container using a password
    """
    responses = iter(['javagat'])  # the default password
    monkeypatch.setattr('getpass.getpass', lambda _: next(responses))
    Kunefe(username="xenon", hostname="localhost", port=10022)
    # assert Kunefe(username="xenon", hostname="localhost", port=10022) == ("Me", "xxx")
