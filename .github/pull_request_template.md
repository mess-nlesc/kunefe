## Checklist before requesting a review
<!-- partly taken from https://axolo.co/blog/p/part-3-github-pull-request-template -->

- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published in downstream modules


## Type of change

Please delete options that are not relevant.

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] This change requires a documentation update

## List of related issues or pull requests**

<!-- add all related issues to the list below-->
Refs:
- #ISSUE_NUMBER_1
- #ISSUE_NUMBER_2

## Describe the changes made in this pull request

Please include a summary of the changes and the related issue. Please also include relevant motivation and context. List any dependencies that are required for this change.

## Instructions to review the pull request**

```shell
# make a new temporary directory and cd into it
cd $(mktemp -d --tmpdir kunefe.XXXXXX)

# get a copy of the repo
git clone https://github.com/mess-nlesc/kunefe .

# checkout the work from this branch
git checkout <this branch>

# create a virtual environment named venv
python3 -m venv venv

# activate the virtual environment
source venv3/bin/activate

# update pip and friends
python3 -m pip install --upgrade pip wheel setuptools

# install runtime dependencies
python3 -m pip install .

# and, if you need it, the development tools
python3 -m pip install .[dev]
```

Keep what you need from below, extend as necessary

```shell
# run the unit tests
pytest

# run linter
ruff .

# add any additional steps for checking

```
