from punish.style import (
    AbstractStyle,
    BadAttributeNameError,
    BadClassNameError,
    MatchSignatureMeta,
    NoLowerCaseMeta,
    NoMixedCaseMeta,
    SignatureError,
    StyleMeta,
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


@pytest.mark.parametrize("object_type", (type, NoLowerCaseMeta, NoMixedCaseMeta, MatchSignatureMeta))
def test_style_meta_instance(object_type: type) -> None:
    assert isinstance(StyleMeta("Stylish", (), {}), object_type)


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
