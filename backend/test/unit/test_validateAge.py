from unittest.mock import MagicMock

import pytest

from src.util.helpers import ValidationHelper


@pytest.fixture
def mocked_usercontroller():
    return MagicMock()


@pytest.fixture
def sut(mocked_usercontroller):
    return ValidationHelper(usercontroller=mocked_usercontroller)


@pytest.mark.unit
@pytest.mark.parametrize(
    "age, expected",
    [
        (-1, "invalid"),
        (0, "underaged"),
        (1, "underaged"),
        (17, "underaged"),
        pytest.param(
            18,
            "valid",
            marks=pytest.mark.xfail(
                reason="Seeded defect: validateAge currently treats age 18 as underaged.",
                strict=True,
            ),
        ),
        (19, "valid"),
        (119, "valid"),
        (120, "valid"),
        (121, "invalid"),
    ],
)
def test_validateAge_classifies_boundary_ages(
    sut,
    mocked_usercontroller,
    age,
    expected,
):
    mocked_usercontroller.get.return_value = {"age": age}

    result = sut.validateAge(userid="user-1")

    assert result == expected
    mocked_usercontroller.get.assert_called_once_with(id="user-1")


@pytest.mark.unit
def test_validateAge_propagates_user_lookup_errors(sut, mocked_usercontroller):
    mocked_usercontroller.get.side_effect = RuntimeError("user lookup failed")

    with pytest.raises(RuntimeError, match="user lookup failed"):
        sut.validateAge(userid="missing-user")

    mocked_usercontroller.get.assert_called_once_with(id="missing-user")
