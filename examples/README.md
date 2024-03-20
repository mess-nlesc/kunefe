<!-- examples/README.md -->
<!-- Run: python examples/test_examples.py -->

# Kunefe examples

The `kunefe` Python module provides functions to run docker images on HPC systems.

Here are a few examples of how to use the functions in `kunefe`:

## Check if a command exists on the host machine

```python
>>> from kunefe import Kunefe
>>> kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
>>> kunefe.check_local_command_exists(command='ls')
True
>>> kunefe.check_local_command_exists(command='thisdoesnotexist')
False

```

## Check required tools to run the package

```python
>>> from kunefe import Kunefe
>>> kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)

>>> kunefe.check_required_tools(['ls', 'rsync', 'cp'])
True

>>> kunefe.check_required_tools(['docker', 'rsync', 'bsxcommand'])
False

```

## Run a shell command

```python
>>> import subprocess
>>> run_command = lambda cmd: subprocess.check_output(cmd, shell=True).decode().strip()
>>> print(run_command('echo $SHELL'))
/bin/bash

>>> print(run_command("date +'%Y'"))
2024

```

