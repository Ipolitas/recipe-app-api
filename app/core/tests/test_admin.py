"""
Tests for the Django admin modifiactions.
"""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestUserAdmin:

    @pytest.fixture(autouse=True)
    def setup(self, client, test_user, admin_user):
        self.test_user = test_user
        self.admin_user = admin_user

        client.force_login(self.admin_user)
        self.client = client

    def test_users_list(self):
        """Test that users are listed on the user page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        assert res.status_code == 200
        assert self.test_user.name in str(res.content)
        assert self.test_user.email in str(res.content)

    def test_edit_user_page(self):
        """Test that the user edit page works."""
        url = reverse('admin:core_user_change', args=[self.test_user.id])
        res = self.client.get(url)

        assert res.status_code == 200
        assert self.test_user.name in str(res.content)
        assert self.test_user.email in str(res.content)

    def test_create_user_page(self):
        """Test that the create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        assert res.status_code == 200
