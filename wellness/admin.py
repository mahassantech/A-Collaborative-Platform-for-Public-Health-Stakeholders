from django.contrib import admin
from .models import WellnessCategory, WellnessPost, WellnessComment

admin.site.register(WellnessCategory)
admin.site.register(WellnessPost)
admin.site.register(WellnessComment)
