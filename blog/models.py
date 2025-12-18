from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from category.models import Category

URGENCY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]

class BlogPost(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="posts"
    )
    title = models.CharField(max_length=200)
    content = RichTextField()  # RichTextField, supports formatting
    description = models.TextField(blank=True, null=True)  # Optional short description
    photo = models.ImageField(upload_to="blog_photos/", blank=True, null=True)
    category = models.ManyToManyField(Category)
    urgency_level = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Latest posts first

    def __str__(self):   
        return f"{self.title} by {self.author.username} ({self.author.role})"


class Comment(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_text = models.TextField()
    is_advice = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def is_doctor(self):
        return self.user.role == "doctor"

    def __str__(self):
        return f"Comment by {self.user.username} ({self.user.role})"
