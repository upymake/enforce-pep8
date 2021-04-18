![Screenshot](icon.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.org/upymake/enforce-pep8.svg?branch=master)](https://travis-ci.org/upymake/enforce-pep8)
[![Coverage Status](https://coveralls.io/repos/github/upymake/enforce-pep8/badge.svg?branch=master)](https://coveralls.io/github/upymake/enforce-pep8?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with pylint](https://img.shields.io/badge/pylint-checked-blue)](https://www.pylint.org)
[![Checked with flake8](https://img.shields.io/badge/flake8-checked-blue)](http://flake8.pycqa.org/)
[![Checked with pydocstyle](https://img.shields.io/badge/pydocstyle-checked-yellowgreen)](http://www.pydocstyle.org/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)
[![PyPI version shields.io](https://img.shields.io/pypi/v/enforce-pep8.svg)](https://pypi.python.org/pypi/enforce-pep8/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/enforce-pep8.svg)](https://pypi.python.org/pypi/enforce-pep8/)
[![CodeFactor](https://www.codefactor.io/repository/github/upymake/enforce-pep8/badge)](https://www.codefactor.io/repository/github/upymake/enforce-pep8)
[![PyPi downloads](https://img.shields.io/pypi/dm/enforce-pep8.svg)](https://pypi.python.org/pypi/enforce-pep8)
[![Downloads](https://pepy.tech/badge/enforce-pep8)](https://pepy.tech/project/enforce-pep8)

# Enforce PEP-8

> Package allows to enforce certain kinds of **PEP-8** convention coding styles (or perform overall code diagnostics).
> It aims to help maintain programmers sanity while making any code changes.
> In large object-oriented programs, it can sometimes be useful to put class definitions under control of a metaclass
> that are used to alert programmers to potential problems.
> 
> Most important that package enforces you to write **clear** and **concise pythonic** code.

## Tools

### Production

- python 3.6, 3.7, 3.8

### Development

- [pytest](https://pypi.org/project/pytest/)
- [black](https://black.readthedocs.io/en/stable/)
- [mypy](http://mypy.readthedocs.io/en/latest)
- [pylint](https://www.pylint.org/)
- [flake8](http://flake8.pycqa.org/en/latest/)
- [pydocstyle](http://www.pydocstyle.org/en/2.1.1/usage.html)
- [interrogate](https://interrogate.readthedocs.io/en/latest)
- [check-manifest](https://pypi.org/project/check-manifest)
- [travis](https://travis-ci.org)

## Usage

### Installation

Please run following script to obtain latest package from PYPI:
```bash
pip install enforce-pep8
✨ 🍰 ✨
```
### Quick start

**Bad class name**: lowercase class name is defined
```python
from punish.style import AbstractStyle


class stylish(AbstractStyle):
     def name(self) -> None:
         pass

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  punish.style.BadClassNameError
Class name 'stylish' specified in lowercase. Consider to use camelcase style!
```

**Bad attribute name**: camelcase method name is defined
```python
from punish.style import AbstractStyle


class Stylish(AbstractStyle):
     def showName(self) -> None:
         pass

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  punish.style.BadAttributeNameError
Bad attribute name is specified: 'Stylish:showName'. Consider to use lowercase style: 'Stylish:showname'! 
```

**Bad method signature**: method signature mismatch within base and child classes
```python
from punish.style import AbstractStyle


class Stylish(AbstractStyle):
     def show(self, indent: str = ":") -> str:
         pass


class SoStylish(Stylish):
    def show(self, indent: str = ":", not_expected_argument: bool = False) -> str:
        pass

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  punish.style.SignatureError
Signature mismatch in 'SoStylish.show', 
(self, indent: str = ':') -> str != (self, indent: str = ':', not_expected_argument: bool = False) -> str 
```

**Duplicated attribute name**: defined two methods with same name
```python
from punish.style import AbstractStyle


class Stylish(AbstractStyle):
    def name(self) -> None:
        pass

    def name(self) -> None:
        pass

Traceback (most recent call last):
  File "<stdin>", line 5, in Stylish
punish.style.DuplicateAttributeError: 'name' attribute is already defined in 'Stylish' class
```

**Bad argument type**: not expected type is passed to the argument
```python
from punish.type import OrderTypedMeta, String, Typed


class Car(metaclass=OrderTypedMeta):
    color: Typed = String()
 
    def __init__(self, color: str) -> None:
        self.color = color


car: Car = Car(color=23)

Traceback (most recent call last):
  File "<stdin>", line 5, in __init__
TypeError: Expected '<class 'str'>' type for 'color' attribute
```

**Bad setter type**: not expected type for setter argument
```python
from punish.type import typed_property


class Person:
    name: property = typed_property("name", str)
    age: property = typed_property("age", int)

    def __init__(self, name: str, age: int) -> None:
        self._name = name
        self._age = age


person: Person = Person(name="Luke", age=22)
person.age = None

Traceback (most recent call last):
  File "<stdin>", line 5, in __init__
TypeError: 'age' argument must be a '<class 'int'>' type
```

**Frozen class attributes**: it is forbidden to modify class attributes 
```python
from punish.type import FrozenMeta


class Bio(metaclass=FrozenMeta):
    name: str = 'Luke'
    company: str = 'Cisco'


bio = Bio()
bio.name = 'Amir'
dataclasses.FrozenInstanceError: cannot assign to field 'name'
```

### Source code

```bash
git clone git@github.com:vyahello/enforce-pep8.git
pip install -e .
```

Or using direct source:
```bash
pip install git+https://github.com/vyahello/enforce-pep8@0.0.1
```
**[⬆ back to top](#enforce-pep-8)**

## Development notes

### Testing

Please execute command below to run unittests with `pytest` tool:
```bash
pytest
```

### CI

Project has Travis CI integration using [.travis.yml](.travis.yml) file thus code analysis (`black`, `pylint`, `flake8`, `mypy`, `pydocstyle`) and unittests (`pytest`) will be run automatically after every made change to the repository.

To be able to run code analysis, please execute command below:
```bash
./analyse-source-code.sh
```
### Release notes

Please check [changelog](CHANGELOG.md) file to get more details about actual versions and it's release notes.

### Meta

Author – _Volodymyr Yahello_. Please check [authors](AUTHORS.md) file for more details.

Distributed under the `MIT` license. See [LICENSE](LICENSE.md) for more information.

You can reach out me at:
* [vyahello@gmail.com](vyahello@gmail.com)
* [https://twitter.com/vyahello](https://twitter.com/vyahello)
* [https://www.linkedin.com/in/volodymyr-yahello-821746127](https://www.linkedin.com/in/volodymyr-yahello-821746127)

### Contributing
I would highly appreciate any contribution and support. If you are interested to add your ideas into project please follow next simple steps:

1. Clone the repository
2. Configure `git` for the first time after cloning with your `name` and `email`
3. `pip install -r requirements.txt` to install all project dependencies
4. `pip install -r requirements-dev.txt` to install all development project dependencies
5. Create your feature branch (git checkout -b feature/fooBar)
6. Commit your changes (git commit -am 'Add some fooBar')
7. Push to the branch (git push origin feature/fooBar)
8. Create a new Pull Request

### What's next

Project is inspired mainly by **pythonic** PEP8 code style reflected at https://www.python.org/dev/peps/pep-0008.
Also decent ideas are described in https://github.com/zedr/clean-code-python project.

In general, future releases will contain API implementations from mentioned style guides above.

All recent activities and ideas are described at project [issues](https://github.com/upymake/enforce-pep8/issues) page. 
If you have ideas you want to change/implement please do not hesitate and create an issue.

**[⬆ back to top](#enforce-pep-8)**
