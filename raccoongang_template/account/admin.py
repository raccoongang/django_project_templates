from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class AccountAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('avatar', 'bdate', 'city', 'country', 'sex',
                       'skype', 'linkedin', 'odnoklassniki', 'vkontakte', 'facebook'),
        }),
    )
