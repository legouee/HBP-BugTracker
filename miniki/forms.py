from django import forms
from .models import WikiPage

class WikiPageForm(forms.ModelForm):
    """Wiki Page edition form"""

    class Meta:
        model = WikiPage
        fields = ['title', 'text', 'ctx']
        widgets = {
            'ctx': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'ng-model': 'wikiPage.title',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control form-control-editor',
                'ng-model': 'wikiPage.text',
            }),
        }