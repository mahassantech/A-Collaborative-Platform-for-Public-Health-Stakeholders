from django.contrib import admin
from .models import CustomUser  # <-- CustomUser import করতে হবে

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role")
    list_filter = ("role",)
    search_fields = ("username", "email")
