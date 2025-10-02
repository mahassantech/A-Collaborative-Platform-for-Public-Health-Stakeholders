from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)   
    description = models.TextField()           
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)   # ক্যাটাগরি (যেমন Health, Travel)
    tags = models.CharField(max_length=250, blank=True, null=True)       # কমা দিয়ে আলাদা করা ট্যাগ

    created_at = models.DateTimeField(auto_now_add=True)  # কখন তৈরি হয়েছে
    updated_at = models.DateTimeField(auto_now=True)      # শেষ কবে আপডেট হয়েছে
    is_published = models.BooleanField(default=True)      # পোষ্ট পাবলিশড কিনা

    def __str__(self):
        return self.title