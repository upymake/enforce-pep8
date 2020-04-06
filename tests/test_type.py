from punish.type import Float, Integer, OrderTypedMeta, String, Typed
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
