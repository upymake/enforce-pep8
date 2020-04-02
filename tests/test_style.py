from punish.style import BadAttributeNameError, MatchSignatureMeta, NoMixedCaseMeta, SignatureError
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


def test_correct_signature() -> None:
    class Base(metaclass=MatchSignatureMeta):
        def check(self, name: str, value: str) -> None:
            pass

    class Sub(Base):
        def check(self, name: str, value: str) -> None:
            pass

    assert Sub()


def test_wrong_signature() -> None:
    class Base(metaclass=MatchSignatureMeta):
        def check(self, name: str, value: str) -> None:
            pass

    with pytest.raises(SignatureError):

        class Sub(Base):
            def check(self, name: str, value: str, keyword: bool = False) -> None:
                pass
