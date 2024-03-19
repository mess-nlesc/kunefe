<!-- Examples.md -->

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

These examples show how to use the `kunefe` module in your code.
