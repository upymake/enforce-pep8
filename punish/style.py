"""Module consists of certain PEP8 punishment conventions in a way of defining metaclasses.

Allows to examine the contents of a class at the time of definition.

Once a PEP8 metaclass has been specified for a class, it gets inherited by all of the subclasses.
"""
from inspect import Signature, signature
from typing import Any, Callable, Dict, Tuple


class BadAttributeNameError(Exception):
    """The class represents bad attribute name exception.

    Commonly occurred when attribute name is out of PEP8 scope.
    """

    def __init__(self, class_name: str, attribute_name: str) -> None:
        super().__init__(
            f"Bad attribute name is specified: '{class_name}:{attribute_name}'. "
            f"Consider to use lowercase style: '{class_name}:{attribute_name.lower()}'!"
        )


class SignatureError(Exception):
    """The class method signature exception.

    Commonly occurred when attribute name is out of PEP8 scope.
    """

    def __init__(self, class_name: str, previous_signature: Signature, current_signature: Signature) -> None:
        super().__init__(f"Signature mismatch in '{class_name}', {previous_signature} != {current_signature}")


class NoMixedCaseMeta(type):
    """A metaclass that rejects any class definition containing attributes with mixed-case names.

    Perhaps as a means for annoying Java/javaScript/etc. programmers.
    """

    def __new__(mcs, class_name: str, bases: Tuple[type, ...], class_dict: Dict[str, Any]) -> Any:
        """Creates and returns new PEP-8 verified object.

        Args:
            class_name (str): name of a class to be created
            bases (tuple): a set of base classes inherited from
            class_dict (dict): class namespace as a dictionary

        Raises:
            `BadAttributeNameError` if name of an attribute is specified in camel-case style e.g fooBar
        """
        for attribute_name in class_dict:  # type: str
            if attribute_name.lower() != attribute_name:
                raise BadAttributeNameError(class_name, attribute_name)
        return super().__new__(mcs, class_name, bases, class_dict)


class MatchSignatureMeta(type):
    """A metaclass that checks the definition of redefined methods.

    Makes sure they have the same calling signature as the original method in the superclass.
    Useful in catching subtle program bugs in argument names.
    """

    def __init__(cls, class_name: str, bases: Tuple[type, ...], class_dict: Dict[str, Any]) -> None:
        super().__init__(class_name, bases, class_dict)
        parent: super = super(cls, cls)
        for name, value in class_dict.items():  # type: str, type
            if name.startswith("_") or not callable(value):
                continue
            previous_defined: Callable[[], Any] = getattr(parent, name, None)
            if previous_defined:
                previous_signature: Signature = signature(previous_defined)
                current_signature: Signature = signature(value)
                if previous_signature != current_signature:
                    raise SignatureError(value.__qualname__, previous_signature, current_signature)