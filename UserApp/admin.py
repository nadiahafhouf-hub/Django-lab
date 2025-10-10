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

    @admin.action(description="Attribuer le rôle 'Organizing Committee' aux utilisateurs sélectionnés")
    def make_committee(self, request, queryset):
        updated = queryset.update(role="comitte")
        self.message_user(request, f"{updated} utilisateur(s) marqué(s) comme membre du comité d’organisation.")

    @admin.action(description="Attribuer le rôle 'Participant' aux utilisateurs sélectionnés")
    def make_participant(self, request, queryset):
        updated = queryset.update(role="participant")
        self.message_user(request, f"{updated} utilisateur(s) marqué(s) comme participant(s).")

    actions = ["make_committee", "make_participant"]


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

    @admin.action(description="Promouvoir en 'Chair'")
    def promote_to_chair(self, request, queryset):
        updated = queryset.update(commitee_role="chair")
        self.message_user(request, f"{updated} membre(s) promu(s) au rôle 'Chair'.")

    @admin.action(description="Rétrograder en 'Member'")
    def demote_to_member(self, request, queryset):
        updated = queryset.update(commitee_role="member")
        self.message_user(request, f"{updated} membre(s) rétrogradé(s) au rôle 'Member'.")

    actions = ["promote_to_chair", "demote_to_member"]

    ordering = ("conference", "commitee_role")

    date_hierarchy = "date_joined"
