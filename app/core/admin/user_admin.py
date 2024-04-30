from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    # Modifies list page
    ordering = ['id']
    list_display = ['email', 'name']
    search_fields = ['email', 'name']

    # Modifies edit page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser',)}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ('last_login',)

    # Modifies add page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
                )
        }),
    )
