# from django.db import models
# from django.conf import settings  # For custom user model
# from blog.models import LANGUAGE_CHOICES


# class Blog(models.Model):
#     LANGUAGE_CHOICES = [
# ('en-US', 'English'),
# ('bn', 'Bangla'),
# ]

# title = models.CharField(max_length=200)
# content = models.TextField()
# description = models.TextField(blank=True, null=True)
# image = models.ImageField(upload_to='blogs/', blank=True, null=True)
# category = models.CharField(max_length=100, blank=True, null=True)
# tags = models.CharField(max_length=250, blank=True, null=True)
# language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='bn')

# # Correct ForeignKey to user
# user = models.ForeignKey(
#     settings.AUTH_USER_MODEL,
#     on_delete=models.CASCADE,
#     related_name='blogs'  # reverse query: user.blogs.all()
# )

# created_at = models.DateTimeField(auto_now_add=True)
# updated_at = models.DateTimeField(auto_now=True)
# is_published = models.BooleanField(default=True)

# def __str__(self):
#     username = self.user.username if self.user else "Unknown User"
#     return f"{self.title} — {username}"
