from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "type_membre", "age", "niveau", "points", "is_staff", "is_superuser")

    fieldsets = UserAdmin.fieldsets + (
        ("Informations personnelles", {
            "fields": ("age", "birth_date", "type_membre", "niveau", "points")
        }),
    )

admin.site.register(User, CustomUserAdmin)


