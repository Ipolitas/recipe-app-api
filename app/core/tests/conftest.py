"""
Shared Pytest fixtures defined for the whole project.
"""
import pytest

from django.contrib.auth import get_user_model


@pytest.fixture()
def client():
    from django.test import Client
    return Client()


@pytest.fixture()
def admin_user(client):
    admin_user = get_user_model().objects.create_superuser(
        email='admin@example.com',
        password='testpass123',
    )
    client.force_login(admin_user)
    yield admin_user


@pytest.fixture()
def test_user(client):
    test_user = get_user_model().objects.create_user(
        email='user@example.com',
        password='testpass123',
        name='Test User',
    )
    client.force_login(test_user)
    yield test_user
