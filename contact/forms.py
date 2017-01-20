from django import forms
from captcha.fields import ReCaptchaField


class ContactForm(forms.Form):
    name = forms.CharField(label="Your Name", max_length=200)
    email = forms.EmailField(label="Your Eamil")
    message = forms.CharField(widget=forms.Textarea)
    captcha = ReCaptchaField()
