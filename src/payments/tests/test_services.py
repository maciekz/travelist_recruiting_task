"""Tests for Services."""
from unittest import mock

import pytest

from payments import services

pytestmark = pytest.mark.django_db


def test_increase_balance(user_with_balance):
    current_balance = user_with_balance.balance
    services.update_user_balance(user_with_balance, 100)
    user_with_balance.refresh_from_db()
    expected = current_balance + 100
    assert user_with_balance.balance == expected


def test_decrease_balance(user_with_balance):
    user_balance = user_with_balance.balance
    services.update_user_balance(user_with_balance, -200)
    user_with_balance.refresh_from_db()
    expected = user_balance - 200
    assert user_with_balance.balance == expected


@mock.patch("payments.services.some_additional_function_to_run_on_balance_update")
def test_update_user_balance_runs_additional_function(
    mock_additional_function, user_with_balance
):
    services.update_user_balance(user_with_balance, 100)
    mock_additional_function.assert_called_once()


@mock.patch("payments.services.some_additional_function_to_run_on_balance_update")
def test_update_user_balance_does_not_run_additional_function(
    mock_additional_function, user_with_balance
):
    services.update_user_balance(user_with_balance, 100, run_additional_function=False)
    mock_additional_function.assert_not_called()
