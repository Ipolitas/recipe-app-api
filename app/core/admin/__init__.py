from django.contrib import admin
from core import models

from .user_admin import UserAdmin
from .recipe_admin import RecipeAdmin


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
