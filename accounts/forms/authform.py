from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )

    def clean(self):
        cleaned_data = super().clean()          # doubt how we are getting data by this 
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password: 
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Invalid username or password")
            self.user = user  # Save user to use in view
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)
