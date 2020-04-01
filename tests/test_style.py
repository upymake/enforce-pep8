from punish.style import BadAttributeNameError, NoMixedCaseMeta
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
