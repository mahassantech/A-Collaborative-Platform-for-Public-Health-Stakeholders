from django.contrib import admin
from .models import BlogPost, Comment, Prescription

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "urgency_level", "created_at")
    search_fields = ("title", "content", "author__username")
    list_filter = ("category", "urgency_level", "created_at")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("blog", "user", "created_at")
    search_fields = ("comment_text", "user__username")

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("blog", "doctor", "created_at")
    search_fields = ("diagnosis", "doctor__username")
