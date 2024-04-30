"""
Tests for recipe APIs.
"""
from decimal import Decimal
from django.urls import reverse

import pytest

from core.models import Recipe
from rest_framework import status
from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
)

RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Return recipe detail URL."""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params):
    """Create a sample recipe object."""
    defaults = {
        'title': 'Sample Recipe',
        'time_minutes': 20,
        'price': Decimal('7.50'),
        'description': 'Sample description',
        'link': 'https://sample.com',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


@pytest.mark.django_db
class TestPublicRecipeAPI:
    """Tests for public recipe endpoints."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client

    def test_auth_required(self):
        """Test auth is required to access the endpoint."""
        res = self.client.get(RECIPES_URL)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPrivateRecipeAPI:
    """Tests for private recipe endpoints."""

    @pytest.fixture(autouse=True)
    def setup(self, test_user, client, test_user_2):
        self.test_user = test_user
        self.client = client
        self.client.force_authenticate(self.test_user)
        self.test_user_2 = test_user_2
        self.recipe_1 = create_recipe(
            user=self.test_user,
            title='Sample Recipe 1'
            )
        self.recipe_2 = create_recipe(
            user=self.test_user,
            title='Sample Recipe 2'
            )

    def test_retrieve_recipes_success(self):
        """Test retrieving list of recipes."""
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

    def test_recipes_limited_to_user(self):
        """Test retrieving recipes only for authenticated user."""
        create_recipe(user=self.test_user_2, title='Sample Recipe User 2')

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.test_user).order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

    def test_recipe_detail_success(self):
        url = detail_url(self.recipe_1.id)

        res = self.client.get(url)
        serializer = RecipeDetailSerializer(self.recipe_1)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

    def test_recipe_list_doesnt_return_description_field(self):
        res = self.client.get(RECIPES_URL)
        assert 'description' not in res.data[0]

    def test_recipe_details_returns_description_field(self):
        url = detail_url(self.recipe_1.id)

        res = self.client.get(url)
        assert 'description' in res.data

    def test_recipe_create_success(self):
        payload = {
            'title': 'Sample Recipe 3',
            'time_minutes': 30,
            'price': Decimal('8.99'),
            'description': 'Sample description 3',
            'link': 'https://sample3.com',
        }

        res = self.client.post(RECIPES_URL, payload)
        recipe = Recipe.objects.get(id=res.data['id'])

        assert res.status_code == status.HTTP_201_CREATED
        for k, v in payload.items():
            assert getattr(recipe, k) == v
        assert recipe.user == self.test_user

    def test_partial_update_recipe_success(self):
        original_description = self.recipe_1.description
        origininal_price = self.recipe_1.price
        payload = {
            'title': 'Updated title',
        }
        url = detail_url(self.recipe_1.id)

        res = self.client.patch(url, payload)

        self.recipe_1.refresh_from_db()
        assert res.status_code == status.HTTP_200_OK
        assert self.recipe_1.title == payload['title']
        assert self.recipe_1.description == original_description
        assert self.recipe_1.price == origininal_price

    def test_recipe_full_update(self):
        payload = {
            'title': 'Updated title',
            'time_minutes': 25,
            'price': Decimal('10.00'),
            'description': 'Updated description',
            'link': 'https://updated.com',
        }
        url = detail_url(self.recipe_1.id)

        res = self.client.put(url, payload)

        self.recipe_1.refresh_from_db()
        assert res.status_code == status.HTTP_200_OK
        for k, v in payload.items():
            assert getattr(self.recipe_1, k) == v
        assert self.recipe_1.user == self.test_user

    def test_recipe_update_user_not_allowed(self):
        payload = {
            'user': self.test_user_2,
        }
        url = detail_url(self.recipe_1.id)

        res = self.client.put(url, payload)

        self.recipe_1.refresh_from_db()
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert self.recipe_1.user == self.test_user

    def test_recipe_delete(self):
        url = detail_url(self.recipe_1.id)

        res = self.client.delete(url)

        assert res.status_code == status.HTTP_204_NO_CONTENT
        assert not Recipe.objects.filter(id=self.recipe_1.id).exists()
