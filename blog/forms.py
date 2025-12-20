from django import forms
from .models import BlogPost, Comment
from ckeditor.widgets import CKEditorWidget
from .models import BlogPost
from crispy_forms.helper import FormHelper
from category.models import Category

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content", "description", "photo", "category", "urgency_level"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "category": forms.SelectMultiple(attrs={"class": "form-select"}),  # Multiple select
            "urgency_level": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

        



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_text"]
        widgets = {
            "comment_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Write a comment..."
                }
            )
        }
