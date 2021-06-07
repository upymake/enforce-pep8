"""Package contains interfaces to enforce PEP8 coding conventions.

It will help to maintain programmers sanity by raising corresponding
exceptions in case of not complying with PEP8 style.

Please check for https://www.python.org/dev/peps/pep-0008/ to get familiar with PEP8 style.
"""
from typing import Tuple
from punish.style import (
    AbstractStyle,
    BadAttributeNameError,
    BadClassNameError,
    DuplicateAttributeError,
    MatchSignatureMeta,
    NoDuplicateMeta,
    NoLowerCaseMeta,
    NoMixedCaseMeta,
    PepStyleMeta,
    SignatureError,
    SingletonMeta,
    abstractstyle,
)
from punish.type import (
    AbstractContextManager,
    Float,
    Integer,
    OrderTypedMeta,
    String,
    Typed,
    enforce_type,
    typed_property,
)

__author__: str = "Volodymyr Yahello"
__email__: str = "vyahello@gmail.com"
__package_name__: str = "enforce-pep8"
__version__: str = "0.0.12"

__all__: Tuple[str, ...] = (
    "AbstractStyle",
    "BadAttributeNameError",
    "BadClassNameError",
    "DuplicateAttributeError",
    "MatchSignatureMeta",
    "NoDuplicateMeta",
    "NoLowerCaseMeta",
    "NoMixedCaseMeta",
    "PepStyleMeta",
    "SignatureError",
    "SingletonMeta",
    "abstractstyle",
    "AbstractContextManager",
    "Float",
    "Integer",
    "OrderTypedMeta",
    "String",
    "Typed",
    "enforce_type",
    "typed_property",
)
