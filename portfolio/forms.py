from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'link']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea, min_length=10)

    # Example extra validation (optional)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Add custom domain rules if you want:
        # if not email.endswith('@example.com'):
        #     raise forms.ValidationError("Please use your @example.com email.")
        return email
