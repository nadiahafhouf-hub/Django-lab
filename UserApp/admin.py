from django.contrib import admin
from .models import User, OrganizingCommittee

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "first_name", "last_name", "email", "role", "affiliation", "nationality", "created_at")

    list_filter = ("role", "nationality", "created_at")

    search_fields = ("username", "first_name", "last_name", "email", "affiliation")

    list_editable = ("role",)

    fieldsets = (
        ("Informations principales", {
            "fields": ("user_id", "username", "first_name", "last_name", "email")
        }),
        ("Détails supplémentaires", {
            "fields": ("affiliation", "nationality", "role")
        }),
        ("Métadonnées", {
            "fields": ("created_at", "updated_at", "last_login", "is_active", "is_staff", "is_superuser")
        }),
    )

    readonly_fields = ("user_id", "created_at", "updated_at", "last_login")

    ordering = ("-created_at",)



@admin.register(OrganizingCommittee)
class OrganizingCommitteeAdmin(admin.ModelAdmin):
    list_display = ("user", "conference", "commitee_role", "date_joined", "created_at")

    list_filter = ("commitee_role", "conference", "date_joined")

    search_fields = ("user__username", "user__first_name", "user__last_name", "conference__name")

    list_editable = ("commitee_role",)

    fieldsets = (
        ("Informations principales", {
            "fields": ("user", "conference", "commitee_role")
        }),
        ("Suivi", {
            "fields": ("date_joined", "created_at", "updated_at")
        }),
    )

    readonly_fields = ("created_at", "updated_at")


    ordering = ("conference", "commitee_role")

    date_hierarchy = "date_joined"

    