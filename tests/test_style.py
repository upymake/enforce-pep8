from punish.style import (
    BadAttributeNameError,
    BadClassNameError,
    MatchSignatureMeta,
    NoLowerCaseMeta,
    NoMixedCaseMeta,
    SignatureError,
)
import pytest


def test_no_mixed_case_meta() -> None:
    class NoMixedCase(metaclass=NoMixedCaseMeta):
        def good_name(self) -> None:
            pass

    assert NoMixedCase()


def test_mixed_case_meta() -> None:
    with pytest.raises(BadAttributeNameError):

        class MixedCase(metaclass=NoMixedCaseMeta):
            def badName(self) -> None:
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
            def check(self, name: str, value: str, keyword: bool = False) -> None:
                pass


def test_no_lower_case_meta() -> None:
    class NoLowerCase(metaclass=NoLowerCaseMeta):
        pass

    assert NoLowerCase()


def test_lower_case_meta() -> None:
    with pytest.raises(BadClassNameError):

        class lowercase(metaclass=NoLowerCaseMeta):
            pass
