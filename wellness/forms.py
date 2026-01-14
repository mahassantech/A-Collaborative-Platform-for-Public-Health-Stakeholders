from django import forms
from .models import WellnessPost, WellnessComment



class WellnessPostForm(forms.ModelForm):
    class Meta:
        model = WellnessPost
        fields = ['title', 'content', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your content here...',
                'rows': 5
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }



class WellnessCommentForm(forms.ModelForm):
    class Meta:
        model = WellnessComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class':'form-control', 'rows':2, 'placeholder':'Write a comment...'})
        }

