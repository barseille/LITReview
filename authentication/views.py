from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.views.generic import View
from . import forms


class LoginPageView(View):
    """
    Classe pour la page de connexion.
    """

    template_name = 'authentication/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        """
        Méthode pour gérer les requêtes GET. Elle initialise un formulaire de connexion vide.
        """
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        """
        Méthode pour gérer les requêtes POST. Elle vérifie l'authenticité des données du formulaire de connexion.
        """
        form = self.form_class(request.POST)

        # si le formulaire respecte les champs requis du model
        if form.is_valid():

            # vérifie s'il existe un utilisateur avec ce nom et ce mot de passe dans la bdd
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None:
                login(request, user)
                return redirect('home')

        message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})


class SignupPageView(View):
    """
    Classe pour la page d'inscription.
    """
    form_class = forms.SignupForm
    template_name = 'authentication/signup.html'

    def get(self, request):
        """
        Méthode pour gérer les requêtes GET. Elle initialise un formulaire d'inscription vide.
        """
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Méthode pour gérer les requêtes POST. Elle vérifie l'authenticité des données du formulaire d'inscription.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, {'form': form})


def logout_user(request):
    """
    Fonction pour déconnecter l'utilisateur actuel. Redirige l'utilisateur vers la page de connexion.
    """
    logout(request)
    return redirect('login')
