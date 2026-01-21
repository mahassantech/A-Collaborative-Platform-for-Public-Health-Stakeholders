from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}  # slug auto-fill
    search_fields = ('name',)  # 🔹 এইটা add করতে হবে autocomplete কাজ করার জন্য
