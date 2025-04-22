from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from shared.admin_utils import ReadOnlyAdmin, ReadOnlyInlineAdmin

from .models import CustomUser, Address, BankCart


@admin.register(Address)
class AddressAdmin(ReadOnlyAdmin):
    pass


@admin.register(BankCart)
class BankCartAdmin(ReadOnlyAdmin):
    pass


class AddressInline(ReadOnlyInlineAdmin):
    model = Address


class BankCartInline(ReadOnlyInlineAdmin):
    model = BankCart


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = (
        "phone_number",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("phone_number", "first_name", "last_name")
    ordering = ("-date_joined",)
    list_filter = ("is_active", "is_staff", "is_superuser")

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = (
        "phone_number",
        "first_name",
        "last_name",
        "last_login",
        "date_joined",
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )

    inlines = [AddressInline, BankCartInline]

    def get_readonly_fields(self, request, obj=None):
        # Make phone_number read-only in both add and edit
        if obj:
            return self.readonly_fields + ("phone_number",)
        return self.readonly_fields
