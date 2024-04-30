from django.contrib import admin


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user']
