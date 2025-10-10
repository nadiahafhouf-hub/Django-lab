from django.contrib import admin
from .models import Session


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "room", "conference", "session_day", "start_time", "end_time", "duration_display")

    def duration_display(self, obj):
        if obj.start_time and obj.end_time:
            delta = obj.end_time - obj.start_time
            hours, remainder = divmod(delta.seconds, 3600)
            minutes = remainder // 60
            return f"{hours}h {minutes}min"
        return "—"
    duration_display.short_description = "Durée"

    list_filter = ("conference", "session_day", "topic", "room")

    search_fields = ("title", "topic", "room", "conference__name")

    list_editable = ("room", "topic")

    fieldsets = (
        ("Informations générales", {
            "fields": ("session_id", "title", "topic", "room")
        }),
        ("Détails de la conférence", {
            "fields": ("conference",)
        }),
        ("Planification", {
            "fields": ("session_day", "start_time", "end_time")
        }),
        ("Suivi", {
            "fields": ("created_at", "updated_at")
        }),
    )

    readonly_fields = ("session_id", "created_at", "updated_at")

    @admin.action(description="Dupliquer les sessions sélectionnées")
    def duplicate_sessions(self, request, queryset):
        for session in queryset:
            session.pk = None  # créer une nouvelle instance
            session.title = f"{session.title} (Copie)"
            session.save()
        self.message_user(request, f"{queryset.count()} session(s) dupliquée(s).")

    actions = ["duplicate_sessions"]

    ordering = ("session_day", "start_time")

    date_hierarchy = "session_day"

