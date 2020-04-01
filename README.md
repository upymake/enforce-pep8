![Screenshot](logo.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.org/vyahello/enforce-pep8.svg?branch=master)](https://travis-ci.org/vyahello/enforce-pep8)
[![Coverage Status](https://coveralls.io/repos/github/vyahello/enforce-pep8/badge.svg?branch=master)](https://coveralls.io/github/vyahello/enforce-pep8?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with pylint](https://img.shields.io/badge/pylint-checked-blue)](https://www.pylint.org)
[![Checked with flake8](https://img.shields.io/badge/flake8-checked-blue)](http://flake8.pycqa.org/)
[![Checked with pydocstyle](https://img.shields.io/badge/pydocstyle-checked-yellowgreen)](http://www.pydocstyle.org/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)
[![PyPI version shields.io](https://img.shields.io/pypi/v/enforce-pep8.svg)](https://pypi.python.org/pypi/enforce-pep8/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/enforce-pep8.svg)](https://pypi.python.org/pypi/enforce-pep8/)

# Enforce PEP-8

> Package allows to enforce certain kinds of PEP-8 convention coding styles (or perform overall code diagnostics).
> It aims to help maintain programmers sanity while making any code changes.
>
> Most important that package enforces you to write **_clear_** and **_concise pythonic_** code.

## Tools

- python 3.6 | 3.7 | 3.8
- code analysis
  - [pytest](https://pypi.org/project/pytest/)
  - [black](https://black.readthedocs.io/en/stable/)
  - [mypy](http://mypy.readthedocs.io/en/latest)
  - [pylint](https://www.pylint.org/)
  - [flake8](http://flake8.pycqa.org/en/latest/)

## Usage

### Installation

Please run following script to obtain latest package from PYPI:
```bash
➜ pip install enforce-pep8
✨ 🍰 ✨
```
### Quick start

### Source code

```bash
➜ git clone git@github.com:vyahello/enforce-pep8.git
➜ pip install -e .
```

Or using direct source:
```bash
➜ pip install git+https://github.com/vyahello/enforce-pep8@0.0.1
```
**[⬆ back to top](#enforce-pep-8)**

## Development notes

### Testing

Please execute command below to run unittests with `pytest` tool:
```bash
➜ pytest
```

### CI

Project has Travis CI integration using [.travis.yml](.travis.yml) file thus code analysis (`black`, `pylint`, `flake8`, `mypy`, `pydocstyle`) and unittests (`pytest`) will be run automatically after every made change to the repository.

To be able to run code analysis, please execute command below:
```bash
➜ ./analyse-source-code.sh
```
### Release notes

Please check [changelog](CHANGELOG.md) file to get more details about actual versions and it's release notes.

### Meta

Author – _Volodymyr Yahello_. Please check [authors](AUTHORS.md) file for more details.

Distributed under the `MIT` license. See [LICENSE](LICENSE.md) for more information.

You can reach out me at:
* [vyahello@gmail.com](vyahello@gmail.com)
* [https://github.com/vyahello](https://github.com/vyahello)
* [https://www.linkedin.com/in/volodymyr-yahello-821746127](https://www.linkedin.com/in/volodymyr-yahello-821746127)

### Contributing
1. clone the repository
2. configure Git for the first time after cloning with your `name` and `email`
3. `pip install -r requirements.txt` to install all project dependencies
4. `pip install -r requirements-dev.txt` to install all development project dependencies

**[⬆ back to top](#enforce-pep-8)**
