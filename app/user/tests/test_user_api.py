"""
Tests for the User API
"""
from django.urls import reverse
from django.contrib.auth import get_user_model

import rest_framework.status as status

import pytest


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """
    Helper function to create a user
    """
    return get_user_model().objects.create_user(**params)


@pytest.mark.django_db
class TestPublicUserAPI():
    """Test the public features of the User API"""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client

    def test_create_user_success(self):
        """Test creating a user with valid payload is successful"""
        payload = {
            'email': 'user@example.com',
            'password': 'testpass123',
            'name': 'Example User',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        assert res.status_code == status.HTTP_201_CREATED
        user = get_user_model().objects.get(email=payload['email'])
        assert user.check_password(payload['password'])
        assert user.name == payload['name']
        assert 'password' not in res.data

    def test_create_user_exists_error(self):
        """Test error returned if user with email already exists"""
        payload = {
            'email': 'user@example.com',
            'password': 'testpass123',
            'name': 'Example User',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user_password_too_short_error(self):
        """Test error returned if password is too short"""
        payload = {
            'email': 'user@example.com',
            'password': 'pw',
            'name': 'Example User',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        assert not user_exists
