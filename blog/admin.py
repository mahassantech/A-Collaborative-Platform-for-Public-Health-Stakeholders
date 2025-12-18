from django.contrib import admin
from .models import BlogPost, Comment

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "author_role", "get_category", "urgency_level", "created_at")
    search_fields = ("title", "content", "author__username")
    list_filter = ("category", "urgency_level", "created_at", "updated_at")
    ordering = ("-created_at",)

    def author_role(self, obj):
        return obj.author.role
    author_role.short_description = "Author Role"

    def get_category(self, obj):
        return obj.category.name if obj.category else "-"
    get_category.short_description = "Category"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("blog", "user", "user_role", "is_advice", "created_at")  # is_advice দেখানো
    search_fields = ("comment_text", "user__username")
    list_filter = ("is_advice", "created_at")  # filter 
    ordering = ("-created_at",)

    def user_role(self, obj):
        return obj.user.role
    user_role.short_description = "User Role"

