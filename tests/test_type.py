from typing import Any, Dict
from punish.type import Float, Integer, OrderTypedMeta, String, Typed, enforce_type, typed_property
import pytest


class __Stock(metaclass=OrderTypedMeta):
    name: Typed = String()
    shares: Typed = Integer()
    price: Typed = Float()

    def __init__(self, name: str, shares: int, price: float) -> None:
        self.name = name
        self.shares = shares
        self.price = price


def test_correctly_typed() -> None:
    assert __Stock(name="foo", shares=10, price=21.1)


@pytest.mark.parametrize(
    "evaluated_type",
    (
        pytest.param(lambda: __Stock(name=None, shares=10, price=21.1), id="String"),
        pytest.param(lambda: __Stock(name="foo", shares=None, price=21.1), id="Integer"),
        pytest.param(lambda: __Stock(name="foo", shares=10, price=None), id="Float"),
    ),
)
def test_badly_typed(evaluated_type: callable) -> None:
    with pytest.raises(TypeError):
        evaluated_type()


def test_enforce_good_type() -> None:
    @enforce_type(foo=bool, bar=int, tez=int)
    def spam(foo: bool, bar: int, tez: int = 42) -> Dict[str, Any]:  # noqa: VNE002
        return locals()

    @enforce_type(foo=bool, bar=int)
    class Spam:
        def __init__(self, foo: bool, bar: int) -> None:  # noqa: VNE002
            self._foo = foo
            self._bar = bar

    assert spam(True, 10)
    assert Spam(True, 10)


def test_enforce_bad_type() -> None:
    @enforce_type(foo=bool, bar=int, tez=int)
    def spam(foo: bool, bar: int, tez: int = 42) -> Dict[str, Any]:  # noqa: VNE002
        return locals()

    with pytest.raises(TypeError):
        spam(None, 10)

    @enforce_type(foo=bool, bar=int)
    class Spam:
        def __init__(self, foo: bool, bar: int) -> None:  # noqa: VNE002
            self._foo = foo
            self._bar = bar

    with pytest.raises(TypeError):
        Spam(None, 10)


def test_nicely_typed_property() -> None:
    class Person:
        age: property = typed_property("age", int)

        def __init__(self, age: int) -> None:
            self._age = age

    person: Person = Person(age=20)
    person.age = 21
    assert person.age == 21


def test_badly_typed_property() -> None:
    class Person:
        age: property = typed_property("age", int)

        def __init__(self, age: int) -> None:
            self._age = age

    with pytest.raises(TypeError):
        Person(age=20).age = None
