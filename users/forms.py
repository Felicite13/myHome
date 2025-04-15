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

class RegisterForm(forms.ModelForm):
    birth_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.TextInput(attrs={
            'placeholder': 'JJ/MM/AAAA'
        }),
        label="Date de naissance"
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'age', 'birth_date', 'type_membre', 'photo']

class UpdatePhotoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['photo']
        labels = {
            'photo': "Ajouter / Modifier la photo de profil"
        }

