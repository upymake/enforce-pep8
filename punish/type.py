"""Module consists of certain type checking punishment conventions in a way of defining metaclasses.

Allows to examine the contents of a class at the time of definition.
"""
from collections import OrderedDict
from functools import wraps
from inspect import Signature, signature
from typing import Any, Callable, Dict, List, Tuple, Type


class Typed:
    """Represents a data type interface.

    Used as a base descriptor type.
    """

    _expected_type: Type[Any] = type(None)

    def __init__(self, name: Any = None) -> None:
        self._name = name

    def __set__(self, instance: Any, value: Any) -> None:
        """Sets space name to value.

        Args:
            instance (Any): an instance of an object
            value (Any): value to be set
        """
        if not isinstance(value, self._expected_type):
            raise TypeError(f"Expected '{self._expected_type}' type for '{self._name}' attribute")
        instance.__dict__[self._name] = value


class Integer(Typed):
    """An integer type.

    A type descriptor.
    """

    _expected_type: Type[int] = int


class Float(Typed):
    """A float type.

    A type descriptor.
    """

    _expected_type: Type[float] = float


class String(Typed):
    """A string type.

    A type descriptor.
    """

    _expected_type: Type[str] = str


class OrderTypedMeta(type):
    """A metaclass for ordered attributes.

    Allows to record the order in which attributes and methods are defined
    inside the class body so the you cna use it in various operations (e.g serializing)

    Captures definition order of descriptions (`Typed` subclassed).
    """

    def __new__(mcs, class_name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]) -> Any:
        """Creates and returns new ordered object.

        Args:
            class_name (str): name of a class to be created
            bases (tuple): a set of base classes inherited from
            namespace (dict): class namespace as a dictionary

        Example:
            >>> class Stock(metaclass=OrderTypedMeta):
            ...    name: Typed = String()
            ...    shares: Typed = Integer()
            ...    price: Typed = Float()
            ...
            ...    def __init__(self, name: str, shares: int, price: float) -> None:
            ...        self.name = name
            ...        self.shares = shares
            ...        self.price = price
            ...
            >>> stock: Stock = Stock(name=None, shared=1, price=200.2)  # raise `TypeError`
        """
        from_namespace: Dict[str, Any] = dict(namespace)
        order: List[Any] = []
        for name, value in from_namespace.items():  # type: str, Any
            if isinstance(value, Typed):
                value._name = name
                order.append(name)
        from_namespace["_order"] = order
        return type.__new__(mcs, class_name, bases, from_namespace)

    @classmethod  # noqa: U100
    def __prepare__(  # type: ignore # noqa: U100
        mcs, class_name: str, bases: Tuple[type, ...]  # pylint: disable=unused-argument
    ) -> Dict[str, Any]:
        """Creates class namespace.

        Invoked immediately at the start of a class definition
        Namespace dictionary is returned.

        Returns `OrderedDict` instead of ordinary dictionary

        Args:
            class_name (str): name of a class to be created
            bases (tuple): a set of base classes inherited from
        """
        return OrderedDict()


def enforce_type(*type_args: Any, **type_kwargs: Any) -> Callable[[Any], Any]:
    """Decorator enforces arguments type checking procedure.

    Args:
        type_args (Any): positional arguments
        type_kwargs (Any): keyword arguments

    Example:
        >>> @enforce_type(int, bool, tez=int)
        ... def spam(foo: int, bar: int, tez: int = 42) -> None:
        ...     pass
        ...
        ...
        ... @enforce_type(bool, int)
        ... class Spam:
        ...      def __init__(self, foo: int, bar: int) -> None:
        ...          self._foo = foo
        ...          self._bar = bar
        ...
        >>> spam(1, 10)  # raise `TypeError`
        >>> new_spam: Spam = Spam(10, 20)  # raise `TypeError`
    """

    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:

        if not __debug__:
            return func

        expected_signature: Signature = signature(func)
        bound_types: Dict[str, Any] = expected_signature.bind_partial(
            *type_args, **type_kwargs
        ).arguments

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for name, value in expected_signature.bind(
                *args, **kwargs
            ).arguments.items():  # type: str, Any
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(f"Argument '{name}' must be '{bound_types[name]}' type")
            return func(*args, **kwargs)  # type: ignore

        return wrapper

    return decorator
