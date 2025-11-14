from django import forms
from .models import Blog
import requests

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'language']

    def clean_content(self):
        content = self.cleaned_data['content']
        lang = self.cleaned_data.get('language', 'bn')

        # Call LanguageTool API
        r = requests.post(
            "https://api.languagetool.org/v2/check",
            data={"text": content, "language": lang}
        ).json()

        if len(r["matches"]) > 15:
            raise forms.ValidationError(
                "Too many grammar mistakes detected. "
                "Please fix your text before submitting."
            )

        return content
