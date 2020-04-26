# pylint: disable-all
from typing import Callable
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
    _AnyCallable,
    abstractstyle,
)
import pytest


def test_no_mixed_case_meta() -> None:
    class SnakeCaseMethod(metaclass=NoMixedCaseMeta):
        def good_name(self) -> None:
            pass

    class Constant(metaclass=NoMixedCaseMeta):
        GOODNAME: str = "foo"

    assert SnakeCaseMethod()
    assert Constant()


def test_mixed_case_meta() -> None:
    with pytest.raises(BadAttributeNameError):

        class CamelCaseMethod(metaclass=NoMixedCaseMeta):
            def badName(self) -> None:
                pass

    with pytest.raises(BadAttributeNameError):

        class CamelCaseVariable(metaclass=NoMixedCaseMeta):
            badName: str = "foo"

    with pytest.raises(BadAttributeNameError):

        class ConstantMethod(metaclass=NoMixedCaseMeta):
            def BADNAME(self) -> None:
                pass


def test_match_signature_meta() -> None:
    class Base(metaclass=MatchSignatureMeta):
        def check(self, name: str, value: str) -> None:
            pass

    class Sub(Base):
        def check(self, name: str, value: str) -> None:
            pass

    assert Sub()


def test_no_match_signature_meta() -> None:
    class Base(metaclass=MatchSignatureMeta):
        def check(self, name: str, value: str) -> None:
            pass

    with pytest.raises(SignatureError):

        class Sub(Base):
            def check(self, name: str, value: str, not_expected_argument: bool = False) -> None:
                pass


def test_no_lower_case_meta() -> None:
    class NoLowerCase(metaclass=NoLowerCaseMeta):
        pass

    assert NoLowerCase()


def test_lower_case_meta() -> None:
    with pytest.raises(BadClassNameError):

        class lowercase(metaclass=NoLowerCaseMeta):
            pass


def test_no_duplicate_meta() -> None:
    class Spam(metaclass=NoDuplicateMeta):
        def name(self) -> None:
            pass

        def age(self) -> None:
            pass

    assert Spam()


def test_duplicate_meta() -> None:

    with pytest.raises(DuplicateAttributeError):

        class Spam(metaclass=NoDuplicateMeta):
            def name(self) -> None:
                pass

            def name(self) -> None:  # noqa: F811
                pass


@pytest.mark.parametrize(
    "object_type", (type, NoLowerCaseMeta, NoMixedCaseMeta, MatchSignatureMeta, NoDuplicateMeta)
)
def test_style_meta_instance(object_type: type) -> None:
    assert isinstance(PepStyleMeta("Stylish", (), {}), object_type)


def test_abstract_style_lower_case():
    with pytest.raises(BadClassNameError):

        class lower(AbstractStyle):
            pass


def test_abstract_style_mixed_case():
    with pytest.raises(BadAttributeNameError):

        class Stylish(AbstractStyle):
            def badName(self) -> None:
                pass


def test_abstract_style_signature():
    class Stylish(AbstractStyle):
        def check(self, name: str) -> None:
            pass

    with pytest.raises(SignatureError):

        class SoStylish(Stylish):
            def check(self, name: str, not_expected_argument: str) -> None:
                pass


def test_abstract_style_duplicate() -> None:
    with pytest.raises(DuplicateAttributeError):

        class Stylish(AbstractStyle):
            def name(self) -> None:
                pass

            def name(self) -> None:  # noqa: F811
                pass


def test_not_singleton_meta() -> None:
    class NotSingleton:
        pass

    assert NotSingleton() is not NotSingleton()


def test_singleton_meta() -> None:
    class Singleton(metaclass=SingletonMeta):
        pass

    assert Singleton() is Singleton() is Singleton()


def test_any_callable() -> None:
    assert isinstance(_AnyCallable, Callable)


def test_abstractstyle() -> None:
    class Base(AbstractStyle):
        @abstractstyle
        def make(self) -> None:
            pass

    class Child(Base):
        pass

    with pytest.raises(TypeError):
        Child()
