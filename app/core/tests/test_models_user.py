"""
Tests for models.
"""
from django.contrib.auth import get_user_model
import pytest


@pytest.mark.django_db
def test_create_user_with_email_successful():
    """Test creating a new user with an email is successful."""
    email = 'test@example.com'
    password = 'testpass123'
    user = get_user_model().objects.create_user(
        email=email,
        password=password
    )

    assert user.email == email
    assert user.check_password(password)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "email,expected", [
        pytest.param('test1@example.com', 'test1@example.com'),
        pytest.param('test2@EXAMPLE.com', 'test2@example.com'),
        pytest.param('Test3@Example.com', 'Test3@example.com'),
        pytest.param('TEST4@EXAMPLE.COM', 'TEST4@example.com'),
        pytest.param('test5@example.COM', 'test5@example.com'),
    ]
)
def test_new_user_email_normalized(email, expected):
    """Test the email for a new user is normalized."""
    user = get_user_model().objects.create_user(email, 'sample123')

    assert user.email == expected


@pytest.mark.django_db
def test_new_user_without_email_raises_error():
    with pytest.raises(ValueError):
        get_user_model().objects.create_user('', 'sample123')


@pytest.mark.django_db
def test_create_new_superuser():
    user = get_user_model().objects.create_superuser(
        'test@example.com',
        'sample123'
        )

    assert user.is_superuser
    assert user.is_staff
