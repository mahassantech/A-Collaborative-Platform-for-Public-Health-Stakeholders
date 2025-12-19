from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser, Specialization


# 🔹 Specialization Admin (VERY IMPORTANT)
@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# 🔹 Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "display_specializations",
        "hospital_name",
        "doctor_license",
        "profile_pic_thumbnail",
    )

    list_filter = ("role", "specialization")
    search_fields = ("username", "email", "hospital_name", "doctor_license")

    # ⚠️ REMOVE readonly specialization
    readonly_fields = ("profile_pic_thumbnail",)

    filter_horizontal = ("specialization",)  # ✅ ManyToMany UI improve

    # ManyToMany display helper
    def display_specializations(self, obj):
        return ", ".join(s.name for s in obj.specialization.all())
    display_specializations.short_description = "Specializations"

    # Profile pic thumbnail
    def profile_pic_thumbnail(self, obj):
        if obj.profile_pic:
            return format_html(
                '<img src="{}" width="40" height="40" '
                'style="object-fit:cover;border-radius:50%;" />',
                obj.profile_pic.url
            )
        return "-"
    profile_pic_thumbnail.short_description = "Profile Pic"
