from django.contrib import admin
from .models import HealthHistory

@admin.register(HealthHistory)
class HealthHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "patient",
        "assigned_doctor",
        "category",
        "is_private",
        "created_at",
    )
    list_filter = ("is_private", "category", "assigned_doctor")
    search_fields = ("title", "patient__username", "assigned_doctor__username")
    autocomplete_fields = ("patient", "assigned_doctor", "category")
