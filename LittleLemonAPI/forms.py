from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignupFrom(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        help_texts = {k:"" for k in fields}

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        if User.objects.filter(username='username', email='email').exists():
            raise forms.ValidationError("Username or Email is not available")

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']