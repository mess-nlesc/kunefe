#!/usr/bin/env python
"""A script to test kunefe module."""

from kunefe import Kunefe

kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)

netlogo_version = "6.3.0"
netlogo_docker_image = f"comses/netlogo:{netlogo_version}"
netlogo_sif_file_name = "netlogo_6.3.0.sif"

# build apptainer image from a Docker image
kunefe.build_apptainer_image(
    docker_image=netlogo_docker_image,
    sif_file_name=netlogo_sif_file_name
)
