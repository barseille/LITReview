from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class LoginForm(forms.Form):
    """
    Formulaire de connexion de l'utilisateur.
    Contient deux champs : nom d'utilisateur et mot de passe.
    """
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')


class SignupForm(UserCreationForm):
    """
    Formulaire d'inscription de l'utilisateur qui hérite de UserCreationForm.
    Utilise le modèle d'utilisateur actif et contient les champs : nom d'utilisateur, email, prénom et nom.
    """
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
