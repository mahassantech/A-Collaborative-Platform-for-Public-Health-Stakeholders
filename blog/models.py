from django.db import models
from django.conf import settings

CATEGORY_CHOICES = [
    ('symptom', 'Symptom'),
    ('treatment', 'Treatment'),
    ('experience', 'Experience'),
    ('question', 'Question'),
    ('advice', 'Advice'),
]

URGENCY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]

class BlogPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    content = models.TextField()
    photo = models.ImageField(upload_to="blog_photos/", blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='experience')
    urgency_level = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='medium')
    tags = models.CharField(max_length=200, blank=True, help_text="Comma separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_doctor(self):
        return self.user.role == "doctor"

    def __str__(self):
        return f"Comment by {self.user.username}"
    

class Prescription(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="prescriptions")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    
    diagnosis = models.TextField()
    medicines = models.TextField()
    tests = models.TextField(blank=True, null=True)
    advice = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription by {self.doctor.username}"
