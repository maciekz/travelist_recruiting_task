import pytest

from payments import factories

pytestmark = pytest.mark.django_db


@pytest.fixture
def user_with_balance():
    return factories.UserWithBalanceFactory()
