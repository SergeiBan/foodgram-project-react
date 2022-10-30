from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from users.forms import AdminForm

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_filter = ('email', 'username')

    def get_form(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get_form(request, *args, **kwargs)
        return AdminForm


admin.site.register(User, CustomUserAdmin)
