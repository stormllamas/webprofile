from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'rows':1}
        ),
        max_length=50,
        required = True,
        )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'rows':1}
        ),
        max_length=50,
        required = True,
        )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={'rows':1}
        ),
        max_length=50,
        required = False,
        help_text='(optional)'
        )

    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={'rows':1}
        ),
        max_length=200,
        required = False,
        )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows':5, 'placeholder': 'What is on your mind?'}
        ),
        max_length=4000,
        help_text='4000 characters allowed',
        required = True,
        )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']