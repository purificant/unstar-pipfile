# unstar-pipfile
If you have stars in your Pipfile, this project is for you!

[![test-workflow](https://github.com/purificant/unstar-pipfile/actions/workflows/test.yaml/badge.svg)](https://github.com/purificant/unstar-pipfile/actions/workflows/test.yaml)
[![PyPI version](https://badge.fury.io/py/unstar-pipfile.svg)](https://badge.fury.io/py/unstar-pipfile)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

`unstar-pipfile` is a tool to scan `Pipfile.lock` and replace any stars in `Pipfile` with precise versions from the lock file.

# Installation
`pip install unstar-pipfile`

# Usage
`python -m unstar_pipfile`
Run as a python module in the directory with `Pipfile` and `Pipfile.lock`.

# Help
`python -m unstar_pipfile --help`
