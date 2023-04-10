from django.contrib import admin
from .forms import TalvidouserChangeForm, TalvidouserCreationForm
from .models import Talvidouser
from django.contrib.auth.admin import UserAdmin


"""Register the talvido user in django admin"""

@admin.register(Talvidouser)
class TalvidouserAdmin(UserAdmin):
    add_form = TalvidouserCreationForm
    form = TalvidouserChangeForm
    model = Talvidouser
    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            "User Information",
            {"fields": ("username", "email", "password", "full_name", "mobile_number")},
        ),
        (
            "User Permissions",
            {"fields": ("is_superuser", "is_staff", "is_active", "user_permissions")},
        ),
        ("Login with", {"fields": ("login_with",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("username",)
    ordering = ("full_name",)
