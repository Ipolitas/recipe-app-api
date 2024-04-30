"""
Shared Pytest fixtures defined for the whole project.
"""
import pytest

from django.contrib.auth import get_user_model


@pytest.fixture()
def client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture()
def admin_user(client):
    admin_user = get_user_model().objects.create_superuser(
        email='admin@example.com',
        password='testpass123',
    )
    yield admin_user


@pytest.fixture()
def test_user(client):
    test_user = get_user_model().objects.create_user(
        email='user@example.com',
        password='testpass123',
        name='Test User',
    )
    yield test_user


@pytest.fixture()
def test_user_2(client):
    test_user_2 = get_user_model().objects.create_user(
        email='user2@example.com',
        password='testpass123',
        name='Test User 2',
    )
    yield test_user_2
