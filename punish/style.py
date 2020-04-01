"""Module consists of certain PEP8 punishment conventions in a way of defining metaclasses.

Allows to examine the contents of a class at the time of definition.

Once a PEP8 metaclass has been specified for a class, it gets inherited by all of the subclasses.
"""
from typing import Any, Dict, Tuple


class BadAttributeNameError(Exception):
    """The class represents bad attribute name exception.

    Commonly occurred when attribute name is out of PEP8 scope.
    """

    def __init__(self, class_name: str, attribute_name: str) -> None:
        super().__init__(
            f"Bad attribute name is specified: '{class_name}:{attribute_name}'. "
            f"Consider to use lowercase style: '{class_name}:{attribute_name.lower()}'!"
        )


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
            `BadAttributeNameError` if name of an attribute is specified in camel-cased style e.g fooBar
        """
        for attribute_name in class_dict:  # type: str
            if attribute_name.lower() != attribute_name:
                raise BadAttributeNameError(class_name, attribute_name)
        return super().__new__(mcs, class_name, bases, class_dict)
