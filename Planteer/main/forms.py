from django import forms
from main.models import Contact

class ContactForm(forms.ModelForm):

    first_name = forms.CharField(
        min_length=2,
        max_length=50,
        error_messages={
            'required': 'First name is required.',
            'min_length': 'First name must be at least 2 characters.',
            'max_length': 'First name must not be more than 50 characters.',
        }
    )

    last_name = forms.CharField(
        min_length=2,
        max_length=50,
        error_messages={
            'required': 'Last name is required.',
            'min_length': 'Last name must be at least 2 characters.',
            'max_length': 'Last name must not be more than 50 characters.',
        }
    )

    email = forms.EmailField(
        error_messages={
            'required': 'Email address is required.',
            'invalid': 'Please enter a valid email address.',
        }
    )

    message = forms.CharField(
        min_length=10,
        max_length=2000,
        widget=forms.Textarea,
        error_messages={
            'required': 'Message is required.',
            'min_length': 'Message must be at least 10 characters.',
            'max_length': 'Message must not be more than 2000 characters.',
        }
    )
    
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email','message']