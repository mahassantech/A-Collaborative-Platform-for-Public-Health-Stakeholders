from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "get_specializations",
        "hospital_name",
        "doctor_license",
        "profile_pic_thumbnail",
    )
    list_filter = ("role", "specialization")
    search_fields = ("username", "email", "hospital_name", "doctor_license")

    readonly_fields = ("doctor_license", "get_specializations")  # verified info read-only in admin

    # ManyToManyField-এর জন্য display helper
    def get_specializations(self, obj):
        return ", ".join([s.name for s in obj.specialization.all()])
    get_specializations.short_description = "Specializations"

    # Profile pic thumbnail
    def profile_pic_thumbnail(self, obj):
        if obj.profile_pic:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit: cover; border-radius:50%;" />',
                obj.profile_pic.url
            )
        return "-"
    profile_pic_thumbnail.short_description = "Profile Pic"
