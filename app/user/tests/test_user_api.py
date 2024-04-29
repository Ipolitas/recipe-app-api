"""
Tests for the User API
"""
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

import rest_framework.status as status

import pytest


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
PROFILE_URL = reverse('user:profile')


def create_user(**params):
    """
    Helper function to create a user
    """
    return get_user_model().objects.create_user(**params)


@pytest.mark.django_db
class TestCreateUserAPI():

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        self.payload = {
            'email': 'user@example.com',
            'password': 'testpass123',
            'name': 'Example User',
        }

    def test_create_user_success(self):
        """Test creating a user with valid payload is successful"""
        res = self.client.post(CREATE_USER_URL, self.payload)

        assert res.status_code == status.HTTP_201_CREATED
        user = get_user_model().objects.get(email=self.payload['email'])
        assert user.check_password(self.payload['password'])
        assert user.name == self.payload['name']
        assert 'password' not in res.data

    def test_create_user_exists_error(self):
        """Test error returned if user with email already exists"""
        create_user(**self.payload)
        res = self.client.post(CREATE_USER_URL, self.payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user_password_too_short_error(self):
        """Test error returned if password is too short"""
        self.payload['password'] = 'pw'
        res = self.client.post(CREATE_USER_URL, self.payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        user_exists = get_user_model().objects.filter(
            email=self.payload['email']
        ).exists()
        assert not user_exists


@pytest.mark.django_db
class TestTokenUserAPI():

    @pytest.fixture(autouse=True)
    def setup(self, client, test_user):
        self.client = client
        self.test_user = test_user

    def test_create_token_success(self):
        """Test that a token is created and returned"""
        payload = {
            'email': self.test_user.email,
            'password': 'testpass123',
        }

        res = self.client.post(TOKEN_URL, payload)

        assert res.status_code == status.HTTP_200_OK
        assert 'token' in res.data
        assert self.test_user.auth_token

    def test_create_token_wrong_password(self):
        """Test that token is not created for invalid credentials"""
        payload = {
            'email': self.test_user.email,
            'password': 'wrongpass',
        }

        res = self.client.post(TOKEN_URL, payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' not in res.data
        with pytest.raises(ObjectDoesNotExist):
            self.test_user.auth_token

    def test_create_token_wrong_email(self):
        """Test that token is not created for invalid email"""
        payload = {
            'email': 'wrong_email@example.com',
            'password': 'testpass123',
        }

        res = self.client.post(TOKEN_URL, payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' not in res.data
        with pytest.raises(ObjectDoesNotExist):
            self.test_user.auth_token

    def test_create_token_blank_password(self):
        """Test that token is not created for blank password"""
        payload = {
            'email': self.test_user.email,
            'password': '',
        }

        res = self.client.post(TOKEN_URL, payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' not in res.data
        with pytest.raises(ObjectDoesNotExist):
            self.test_user.auth_token

    def test_retrieve_profile_authorized_succeeds(self):
        """Test that user is returned when authenticated"""
        self.client.force_authenticate(self.test_user)
        res = self.client.get(PROFILE_URL)
        assert res.status_code == status.HTTP_200_OK
        assert res.data['email'] == self.test_user.email
        assert res.data['name'] == self.test_user.name

    def test_retrieve_profile_unauthorized_fails(self):
        """Test that authentication is enforced"""
        res = self.client.get(PROFILE_URL)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestProfileUserAPI():

    @pytest.fixture(autouse=True)
    def setup(self, client, test_user):
        self.test_user = test_user
        client.force_authenticate(self.test_user)
        self.client = client

    def test_retrieve_profile_success(self):
        """Test retrieving profile"""
        res = self.client.get(PROFILE_URL)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == {
            'email': self.test_user.email,
            'name': self.test_user.name,
        }

    def test_post_profile_not_allowed(self):
        """Test that POST is not allowed on the me URL"""
        res = self.client.post(PROFILE_URL, {})

        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_profile_not_allowed(self):
        """Test that DELETE is not allowed on the me URL"""
        res = self.client.delete(PROFILE_URL)

        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {
            'name': 'New Name',
            'password': 'newpass123',
        }

        res = self.client.patch(PROFILE_URL, payload)

        assert res.status_code == status.HTTP_200_OK
        self.test_user.refresh_from_db()
        assert self.test_user.name == payload['name']
        assert self.test_user.check_password(payload['password'])
