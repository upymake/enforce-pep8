"""Module consists of certain PEP8 punishment conventions in a way of defining metaclasses.

Allows to examine the contents of a class at the time of definition.

Once a PEP8 metaclass has been specified for a class, it gets inherited by all of the subclasses.
"""
import abc
import re
from collections import OrderedDict
from inspect import Signature, signature
from typing import Any, Callable, Dict, Optional, Tuple

_AnyCallable = Callable[..., Any]


def abstractstyle(callable_object: _AnyCallable) -> _AnyCallable:
    """A decorator indicating abstract style methods.

    An AbstractStyle class cannot be instantiated unless all of its abstract methods are overridden.

    Args:
        callable_object (Callable[[Any, ...], Any]):

    Returns:
        a callable object

    Example:
        >>> class Base(AbstractStyle):
        ...     @abstractstyle
        ...     def name(self) -> None:
        ...         pass
        ...
        ...
        ...     class Child(Base):
        ...         pass
        ...
        ...
        >>> Child()
        ... TypeError: Can't instantiate abstract class Base with abstract methods name
    """
    return abc.abstractmethod(callable_object)


class BadAttributeNameError(Exception):
    """The class represents bad attribute name exception.

    Commonly occurred when attribute name is out of PEP8 scope.
    """

    def __init__(self, class_name: str, attribute_name: str) -> None:
        super().__init__(
            f"Bad attribute name is specified: '{class_name}:{attribute_name}'. "
            f"Consider to use lowercase style: '{class_name}:{attribute_name.lower()}'!"
        )


class BadClassNameError(Exception):
    """The class represents bad class name exception.

    Commonly occurred when attribute name is out of PEP8 scope.
    """

    def __init__(self, class_name: str) -> None:
        super().__init__(
            f"Class name '{class_name}' specified in lowercase. Consider to use camelcase style!"
        )


class SignatureError(Exception):
    """The class method signature exception.

    Commonly occurred when attribute name is out of PEP8 scope.
    """

    def __init__(
        self, class_name: str, previous_signature: Signature, current_signature: Signature
    ) -> None:
        super().__init__(
            f"Signature mismatch in '{class_name}', {previous_signature} != {current_signature}"
        )


class DuplicateAttributeError(Exception):
    """The class represents duplicated attribute exception.

    Commonly occurred when attribute name is out of PEP8 scope.
    """

    def __init__(self, attribute_name: str, class_name: str) -> None:
        super().__init__(f"'{attribute_name}' attribute is already defined in '{class_name}' class")


class NoMixedCaseMeta(type):
    """A metaclass that rejects any class definition containing attributes with mixedcase names.

    Perhaps as a means for annoying Java/javaScript/etc. programmers.
    """

    __camelcase_pattern: str = "([a-z]+[A-Z]+).*"

    def __new__(mcs, class_name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]) -> Any:
        """Creates and returns new PEP-8 verified object.

        Args:
            class_name (str): name of a class to be created
            bases (tuple): a set of base classes inherited from
            namespace (dict): class namespace as a dictionary

        Raises:
            `BadAttributeNameError` if name of an attribute is specified in mixedcase style e.g fooBar
        """
        for attr_name, value in namespace.items():  # type: str, Any
            if re.compile(mcs.__camelcase_pattern).match(attr_name) or (
                attr_name.isupper() and callable(value)
            ):
                raise BadAttributeNameError(class_name, attr_name)
        return super().__new__(mcs, class_name, bases, namespace)


class NoLowerCaseMeta(type):
    """A metaclass that rejects any class definition containing classes with lower-case names."""

    def __new__(mcs, class_name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]) -> Any:
        """Creates and returns new PEP-8 verified object.

        Args:
            class_name (str): name of a class to be created
            bases (tuple): a set of base classes inherited from
            namespace (dict): class namespace as a dictionary

        Raises:
            `BadClassNameError` if name of a class is specified in lowercase style e.g foo
        """
        if class_name[0].islower() or class_name.islower():
            raise BadClassNameError(class_name)
        return super().__new__(mcs, class_name, bases, namespace)


class MatchSignatureMeta(type):
    """A metaclass that checks the definition of redefined methods.

    Makes sure they have the same calling signature as the original method in the superclass.
    Useful in catching subtle program bugs in argument names.
    """

    def __init__(cls, class_name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]) -> None:
        """Instantiates new PEP-8 verified object.

        Args:
            class_name (str): name of a class to be created
            bases (tuple): a set of base classes inherited from
            namespace (dict): class namespace as a dictionary

        Raises:
            `SignatureError` if method signatures of base and super classes don't match
        """
        super().__init__(class_name, bases, namespace)
        parent: super = super(cls, cls)
        for name, value in namespace.items():  # type: str, type
            if name.startswith("_") or not callable(value):
                continue
            previous_defined: Callable[[], Any] = getattr(parent, name, None)
            if previous_defined:
                previous_signature: Signature = signature(previous_defined)
                current_signature: Signature = signature(value)
                if previous_signature != current_signature:
                    raise SignatureError(value.__qualname__, previous_signature, current_signature)


class NoDuplicateDict(OrderedDict):  # type: ignore
    """Represents no duplicated ordered dictionary."""

    def __init__(self, class_name: str) -> None:
        self._class_name = class_name
        super().__init__()

    def __setitem__(self, attribute_name: str, value: Any) -> None:
        """Sets given name to value into class namespace.

        Args:
            attribute_name (str): name of an attribute
            value (Any): name of a value

        Raises:
            `DuplicatedAttributeError` if name is already defined in class namespace
        """
        if attribute_name in self:
            raise DuplicateAttributeError(attribute_name, self._class_name)
        super().__setitem__(attribute_name, value)


class NoDuplicateMeta(type):
    """A metaclass rejects defined duplicated attributes in a class."""

    def __new__(mcs, class_name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]) -> Any:
        """Creates and returns new object.

        Args:
            class_name (str): name of a class to be created
            bases (tuple): a set of base classes inherited from
            namespace (dict): class namespace as a dictionary

        Example:
            >>> class Spam(metaclass=NoDuplicateMeta):
            ...     def name(self) -> None:
            ...         pass
            ...
            ...     def name(self) -> None:
            ...         pass
            ...
            ... TypeError: 'name' attribute is already defined in 'Spam' class
        """
        from_namespace: Dict[str, Any] = dict(namespace)
        from_namespace["_order"] = [name for name in namespace if not name.startswith("_")]
        return type.__new__(mcs, class_name, bases, from_namespace)

    @classmethod  # noqa: U100
    def __prepare__(  # type: ignore # noqa: U100
        mcs, class_name: str, bases: Tuple[type, ...]  # pylint: disable=unused-argument
    ) -> Dict[str, Any]:
        """Creates class namespace.

        Invoked immediately at the start of a class definition.
        Namespace dictionary is returned.

        Args:
            class_name (str): name of a class to be created
            bases (tuple): a set of base classes inherited from
        """
        return NoDuplicateDict(class_name)


class PepStyleMeta(
    abc.ABCMeta, NoLowerCaseMeta, NoMixedCaseMeta, MatchSignatureMeta, NoDuplicateMeta
):
    """A metaclass forces PEP-8 convention coding styles.

    Examines the contents of a class at the time of definition.
    Enforces certain kinds of coding conventions to help maintains programmer sanity.

    In general, following items are forbidden:
      - not overridden abstract methods
      - define camel-case attribute & method names
      - define lower-case
      - redefine methods with wrong signature
      - duplicated attributes

    It will raise corresponding exception while class definition procedure.
    """

    pass


class AbstractStyle(metaclass=PepStyleMeta):
    """The class represents abstract base class to enforce PEP8 coding style conventions.

    Derive from it to make PEP8 coding punishment (it will make effect while definition) e.g:

    >>> class Root(AbstractStyle):
    ...    pass
    ...
    ...
    ...  class Child(Root):
    ...    pass
    ...
    >>>
    """

    pass


class SingletonMeta(type):
    """A metaclass that makes from class object a singleton unity.

    It will be instantiated only once.
    """

    def __init__(cls, class_name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]) -> None:
        """Initializes a singleton object.

        Args:
            class_name (str): name of a class to be created
            bases (tuple): a set of base classes inherited from
            namespace (dict): class namespace as a dictionary
        """
        cls.__instance: Optional["SingletonMeta"] = None
        super().__init__(class_name, bases, namespace)

    def __call__(cls, *args: Any, **kwargs: Any) -> "SingletonMeta":
        """Calls an instance of a singleton.

        Calling when instance is created e.g:

        >>> class Foo(metaclass=SingletonMeta):
        ...     pass
        ...
        >>> foo = Foo()  # `__call__` metaclass method is called here
        <__main__.Foo object at 0x1064bb220>
        >>>

        Args:
            args (Any): positional arguments
            kwargs (Any): keyword arguments
        """
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance
        return cls.__instance
