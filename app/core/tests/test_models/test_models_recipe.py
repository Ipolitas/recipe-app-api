"""
Tests for Recipe model.
"""
from decimal import Decimal

from django.db import IntegrityError
import pytest

from core.models import Recipe


@pytest.mark.django_db
class TestRecipeModel:

    @pytest.fixture(autouse=True)
    def setup(self, test_user):
        self.test_user = test_user

    def test_create_recipe_success(self):
        recipe = Recipe.objects.create(
            user=self.test_user,
            title='Test Recipe',
            time_minutes=10,
            price=Decimal('5.50'),
            description='Test description',
        )

        assert str(recipe) == recipe.title

    def test_create_recipe_without_user_raises_error(self):
        with pytest.raises(IntegrityError):
            Recipe.objects.create(
                user=None,
                title='Test Recipe',
                time_minutes=10,
                price=Decimal('5.50'),
                description='Test description',
            )
