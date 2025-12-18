from django import forms
from .models import BlogPost, Comment
from ckeditor.widgets import CKEditorWidget
from .models import BlogPost
from category.models import Category


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content", "description", "photo", "category", "urgency_level"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "category": forms.Select(attrs={"class": "form-select"}),  # select box
            "urgency_level": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # category queryset শুধু active/সব category দেখাতে
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Select Category"  # placeholder
        
        
class CommentForm(forms.ModelForm):
    comment_text = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Add a comment..."}))
    
    class Meta:
        model = Comment
        fields = ["comment_text"]  # is_advice field hidden, set in view

