from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'age',
            'birth_date',
            'type_membre',
            'photo',  
            'password1',
            'password2',
        ]
        labels = {
            'username': 'Pseudonyme',
            'email': 'Adresse e-mail',
            'age': 'Âge',
            'birth_date': 'Date de naissance',
            'type_membre': 'Type de membre',
            'photo': 'Photo de profil',  
            'password1': 'Mot de passe',
            'password2': 'Confirmation du mot de passe',
        }

