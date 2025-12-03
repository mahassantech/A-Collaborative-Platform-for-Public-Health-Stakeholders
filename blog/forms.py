from django import forms
from .models import BlogPost, Comment, Prescription

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content", "photo", "category", "urgency_level", "tags"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_text"]

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["diagnosis", "medicines", "tests", "advice"]
