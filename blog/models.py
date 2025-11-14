from django.db import models

class Blog(models.Model):
    LANGUAGE_CHOICES = [
        ('en-US', 'English'),
        ('bn', 'Bangla'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='bn')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
