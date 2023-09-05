"""Tests for Views."""

from http import HTTPStatus
from unittest import mock

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    from django.test import Client

    return Client()


def test_open_empty_user_list_view(client):
    """Test opening an empty user list."""
    url = reverse("user_list")
    resp = client.get(url)
    # Verify response status
    assert resp.status_code == HTTPStatus.OK


def test_open_user_list_view(client, user_with_balance):
    """Test opening an empty user list."""
    url = reverse("user_list")
    resp = client.get(url)
    # Verify response status
    assert resp.status_code == HTTPStatus.OK


def test_open_non_existing_user_form(client):
    """Test opening a form for non-existent user."""
    url = reverse("user_balance_update", kwargs={"pk": 1})
    resp = client.get(url)
    # Verify response status
    assert resp.status_code == HTTPStatus.NOT_FOUND


def test_open_existing_user_form(client, user_with_balance):
    """Test opening a form for existing user."""
    url = reverse("user_balance_update", kwargs={"pk": user_with_balance.id})
    resp = client.get(url)
    # Verify response status
    assert resp.status_code == HTTPStatus.OK


@mock.patch("payments.views.update_user_balance")
def test_submit_existing_user_form(mock_service_function, client, user_with_balance):
    """Test opening an empty user list."""
    url = reverse("user_balance_update", kwargs={"pk": user_with_balance.id})
    request_data = {
        "balance_change": 100,
        "balance_update_reason": "others",
    }
    resp = client.post(url, request_data)
    # Verify response
    assert resp.status_code == HTTPStatus.FOUND
    assert resp.url == url
    # Verify that service function has been called
    mock_service_function.assert_called_once_with(user_with_balance, 100)
