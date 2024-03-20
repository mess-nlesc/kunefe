<!-- examples/README.md -->
<!-- Run: python -m doctest -v examples/README.md -->

# Kunefe examples

The `kunefe` Python module provides functions to run docker images on HPC systems.

Here are a few examples of how to use the functions in `kunefe`:

## initialization

```python
>>> from kunefe import Kunefe
>>> kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)

```

## Check if a command exists on the host machine

```python
>>> kunefe.check_local_command_exists(command='ls')
True
>>> kunefe.check_local_command_exists(command='thisdoesnotexist')
False

```

## Check required tools to run the package

```python
>>> kunefe.check_required_tools(['ls', 'rsync', 'cp'])
True

>>> kunefe.check_required_tools(['docker', 'rsync', 'bsxcommand'])
False

```

## Extra: Run a shell command

```python
>>> import subprocess
>>> run_command = lambda cmd: subprocess.check_output(cmd, shell=True).decode().strip()

```

```python
>>> print(run_command("date +'%Y'"))
2024

```

## Copy files


