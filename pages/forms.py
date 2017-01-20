from django import forms

from .models.pages import Page


class NewPageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title']
    
