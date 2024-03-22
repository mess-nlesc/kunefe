# Kunefe

Kunefe is a Python package that helps users run Docker containers on HPC systems. It can:

- convert an existing Docker image into an Apptainer image
- generate scripts for batch jobs to run containerized images
- submit jobs to HPC batch queues (SLURM)
- connect to a remote host via SSH and run commands
- copy and retrieve files from a remote system
- monitor the job queue

## Requirements

### The host system requirements (e.g. your laptop or desktop computer):

- [Docker](https://docs.docker.com/engine/install/)
- [Apptainer](https://apptainer.org/docs/admin/main/installation.html)
- [Python 3](https://www.python.org/downloads/)

### Remote system requirements:

- [Apptainer](https://apptainer.org/docs/admin/main/installation.html)
- [SSH server](https://www.openssh.com/)
- [Slurm Workload Manager](https://slurm.schedmd.com/documentation.html)

**Note:** If Apptainer is not available on the remote system, it can be installed using kunefe which will require the following packages to be installed on the remote system: `curl rpm2cpio cpio`

## Badges

[![Tests](https://github.com/mess-nlesc/kunefe/actions/workflows/tests.yml/badge.svg)](https://github.com/mess-nlesc/kunefe/actions/workflows/tests.yml)
[![Examples](https://github.com/mess-nlesc/kunefe/actions/workflows/examples.yml/badge.svg)](https://github.com/mess-nlesc/kunefe/actions/workflows/examples.yml)
[![Documentation Status](https://readthedocs.org/projects/kunefe/badge/?version=latest)](https://kunefe.readthedocs.io/en/latest/?badge=latest)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/kunefe.svg)](https://pypi.python.org/pypi/kunefe/)
![](https://img.shields.io/badge/windows%20%7C%20macos%20%7C%20linux-grey)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

<!-- [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pydocstyle](https://img.shields.io/badge/pydocstyle-enabled-AD4CD3)](http://www.pydocstyle.org/en/stable/) -->


| fair-software.eu recommendations | |
| :-- | :--  |
| howfairis                          | [![fair-software badge](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow)](https://fair-software.eu) |
| (1/5) code repository              | [![github repo badge](https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue)](https://github.com/mess-nlesc/kunefe) |
| (2/5) license                      | [![github license badge](https://img.shields.io/github/license/mess-nlesc/kunefe)](https://github.com/mess-nlesc/kunefe) |
| (3/5) community registry           | [![RSD](https://img.shields.io/badge/rsd-kunefe-00a3e3.svg)](https://www.research-software.nl/software/kunefe) [![workflow pypi badge](https://img.shields.io/pypi/v/kunefe.svg?colorB=blue)](https://pypi.python.org/project/kunefe/) |
| (4/5) citation                     | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10786467.svg)](https://zenodo.org/doi/10.5281/zenodo.10786467)
 | (5/5) checklist                    | [![OpenSSF Best Practices](https://www.bestpractices.dev/projects/8629/badge)](https://www.bestpractices.dev/projects/8629) |

<details>
<summary>
  <span style="font-size:1.4em; font-weight: bold;">
    🚀 Click to see all the badges
  </span>
</summary>
<br>

| Code quality | |
| :-- | :--  |
| Static analysis                    | [![workflow scq badge](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=alert_status)](https://sonarcloud.io/dashboard?id=mess-nlesc_kunefe) [![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) [![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) [![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) [![Bugs](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=bugs)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) [![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) |
| Coverage                           | [![workflow scc badge](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=coverage)](https://sonarcloud.io/dashboard?id=mess-nlesc_kunefe) |


| **GitHub Actions**                 | &nbsp; |
| :-- | :--  |
| Build                              | [![build](https://github.com/mess-nlesc/kunefe/actions/workflows/build.yml/badge.svg)](https://github.com/mess-nlesc/kunefe/actions/workflows/build.yml) |
| Howfairis                              | [![build](https://github.com/mess-nlesc/kunefe/actions/workflows/howfairis.yml/badge.svg)](https://github.com/mess-nlesc/kunefe/actions/workflows/howfairis.yml) |
| Citation data consistency          | [![cffconvert](https://github.com/mess-nlesc/kunefe/actions/workflows/cffconvert.yml/badge.svg)](https://github.com/mess-nlesc/kunefe/actions/workflows/cffconvert.yml) |
| SonarCloud                         | [![sonarcloud](https://github.com/mess-nlesc/kunefe/actions/workflows/sonarcloud.yml/badge.svg)](https://github.com/mess-nlesc/kunefe/actions/workflows/sonarcloud.yml) |
| MarkDown link checker              | [![markdown-link-check](https://github.com/mess-nlesc/kunefe/actions/workflows/markdown-link-check.yml/badge.svg)](https://github.com/mess-nlesc/kunefe/actions/workflows/markdown-link-check.yml) |

</details>

## Installation

To install the latest kunefe release from PyPI, run:

```console
python -m pip kunefe
```

To install the development version of kunefe from GitHub repository, do:

```console
python -m pip  install git+https://github.com/mess-nlesc/kunefe.git@main
```

## Examples

See the examples in [`examples`](examples) folder.

## Documentation

See [https://readthedocs.org/projects/kunefe/](https://readthedocs.org/projects/kunefe/) for the code documentation.

## The project setup

The project setup is documented in [project_setup.md](project_setup.md). Feel free to remove this document (and/or the link to this document) if you don't need it.

## Contributing

If you want to contribute to the development of kunefe,
have a look at the [contribution guidelines](CONTRIBUTING.md).

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [NLeSC/python-template](https://github.com/NLeSC/python-template).
