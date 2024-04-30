"""
Database model for Recipe object.
"""
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title
