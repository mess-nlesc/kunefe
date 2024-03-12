# Kunefe

Kunefe is a Python package that helps users run containers on HPC systems. It can:

- convert Docker images into a Apptainer image
- generate scripts for batch jobs to run Docker images
- submit jobs to HPC batch queues (SLURM)
- connect to a remote host via SSH and run commands
- copy and retrieve files from a remote system

## Badges

| fair-software.eu recommendations | |
| :-- | :--  |
| (1/5) code repository              | [![github repo badge](https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue)](https://github.com/mess-nlesc/kunefe) |
| (2/5) license                      | [![github license badge](https://img.shields.io/github/license/mess-nlesc/kunefe)](https://github.com/mess-nlesc/kunefe) |
| (3/5) community registry           | [![RSD](https://img.shields.io/badge/rsd-kunefe-00a3e3.svg)](https://www.research-software.nl/software/kunefe) [![workflow pypi badge](https://img.shields.io/pypi/v/kunefe.svg?colorB=blue)](https://pypi.python.org/project/kunefe/) |
| (4/5) citation                     | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10786467.svg)](https://zenodo.org/doi/10.5281/zenodo.10786467)
 | (5/5) checklist                    | [![OpenSSF Best Practices](https://www.bestpractices.dev/projects/8629/badge)](https://www.bestpractices.dev/projects/8629) |
| howfairis                          | [![fair-software badge](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow)](https://fair-software.eu) |
| **Other best practices**           | &nbsp; |
| Static analysis                    | [![workflow scq badge](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=alert_status)](https://sonarcloud.io/dashboard?id=mess-nlesc_kunefe) [![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) [![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) [![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) [![Bugs](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=bugs)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) [![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=mess-nlesc_kunefe) |
| Coverage                           | [![workflow scc badge](https://sonarcloud.io/api/project_badges/measure?project=mess-nlesc_kunefe&metric=coverage)](https://sonarcloud.io/dashboard?id=mess-nlesc_kunefe) |
| Documentation                      | [![Documentation Status](https://readthedocs.org/projects/kunefe/badge/?version=latest)](https://kunefe.readthedocs.io/en/latest/?badge=latest) |
| **GitHub Actions**                 | &nbsp; |
| Build                              | [![build](https://github.com/mess-nlesc/kunefe/actions/workflows/build.yml/badge.svg)](https://github.com/mess-nlesc/kunefe/actions/workflows/build.yml) |
| Howfairis                              | [![build](https://github.com/mess-nlesc/kunefe/actions/workflows/howfairis.yml/badge.svg)](https://github.com/mess-nlesc/kunefe/actions/workflows/howfairis.yml) |
| Citation data consistency          | [![cffconvert](https://github.com/mess-nlesc/kunefe/actions/workflows/cffconvert.yml/badge.svg)](https://github.com/mess-nlesc/kunefe/actions/workflows/cffconvert.yml) |
| SonarCloud                         | [![sonarcloud](https://github.com/mess-nlesc/kunefe/actions/workflows/sonarcloud.yml/badge.svg)](https://github.com/mess-nlesc/kunefe/actions/workflows/sonarcloud.yml) |
| MarkDown link checker              | [![markdown-link-check](https://github.com/mess-nlesc/kunefe/actions/workflows/markdown-link-check.yml/badge.svg)](https://github.com/mess-nlesc/kunefe/actions/workflows/markdown-link-check.yml) |

## Installation

To install the latest kunefe release from PyPI, run:

```console
python -m pip kunefe
```

To install the development version of kunefe from GitHub repository, do:

```console
git clone git@github.com:mess-nlesc/kunefe.git
cd kunefe
python -m pip install .
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
