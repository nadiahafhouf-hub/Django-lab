from django.contrib import admin
from .models import Conference, Submission

# Personnalisation du header de l’administration
admin.site.site_header = "Conference Management Admin"
admin.site.site_title = "Conference Dashboard"
admin.site.index_title = "Welcome to Conference Management Admin Panel"


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("title", "short_abstract", "status", "user_id", "conference_id", "submission_date", "payed")

    def short_abstract(self, obj):
        return (obj.abstract[:50] + "...") if len(obj.abstract) > 50 else obj.abstract
    short_abstract.short_description = "Résumé (50c)"

    list_filter = ("status", "payed", "conference_id", "submission_date")

    search_fields = ("title", "keywords", "user__username")

    list_editable = ("status", "payed")

    fieldsets = (
        ("Infos générales", {
            "fields": ("submission_id", "title", "abstract", "keywords")
        }),
        ("Fichier et conférence", {
            "fields": ("paper", "conference")
        }),
        ("Suivi", {
            "fields": ("status", "payed", "submission_date", "user")
        }),
    )

    readonly_fields = ("submission_id", "submission_date")

    @admin.action(description="Marquer comme payées les soumissions sélectionnées")
    def mark_as_payed(self, request, queryset):
        updated = queryset.update(payed=True)
        self.message_user(request, f"{updated} soumission(s) marquée(s) comme payée(s).")

    @admin.action(description="Accepter les soumissions sélectionnées")
    def mark_as_accepted(self, request, queryset):
        updated = queryset.update(status="Accepted")
        self.message_user(request, f"{updated} soumission(s) acceptée(s).")

    actions = ["mark_as_payed", "mark_as_accepted"]



class SubmissionInline(admin.StackedInline):
    model = Submission
    extra = 1
    fields = ("title", "status", "user", "payed")
    readonly_fields = ("submission_id",)
    show_change_link = True


@admin.register(Conference)
class AdminPerso(admin.ModelAdmin):
    list_display = ("name", "theme", "location", "start_date", "end_date", "duration")
    ordering = ("start_date",)
    list_filter = ("theme", "location", "end_date")
    search_fields = ("name",)
    readonly_fields = ("conference_id",)
    date_hierarchy = "start_date"

    fieldsets = (
        ("Informations générales", {
            "fields": ("conference_id", "name", "theme", "description")
        }),
        ("Logistique", {
            "fields": ("location", "start_date", "end_date")
        }),
    )

    inlines = [SubmissionInline]

    def duration(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return "RAS"
    duration.short_description = "Durée (jours)"


