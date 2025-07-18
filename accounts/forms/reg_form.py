from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import User  # your custom User model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # ✅ your custom user model
        fields = ('username', 'email')  # add any fields you want