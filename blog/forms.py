from django import forms
from . import models
from django.contrib.auth import get_user_model


class TicketForm(forms.ModelForm):
    """Formulaire pour la création et la modification de ticket"""
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        labels = {"title": "Titre du ticket"}

    def __init__(self, *args, **kwargs):
        """Initialise le champ image en tant que champ de sélection de fichier."""
        super().__init__(*args, **kwargs)
        self.fields['image'].widget = forms.FileInput()


class DeleteTicketForm(forms.Form):
    """Formulaire pour la suppression de ticket"""
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class SubscribeForm(forms.Form):
    """Formulaire pour l'abonnement à d'autres utilisateurs"""
    user = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class ReviewForm(forms.ModelForm):
    """Formulaire pour la création et la modification de critique"""
    RATING_CHOICES = [
        (1, '1 - Mauvais'),
        (2, '2 - Faible'),
        (3, '3 - Moyen'),
        (4, '4 - Bien'),
        (5, '5 - Excellent')
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label="Évaluation")

    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']
        labels = {
            'headline': 'Titre de la critique',
            'body': 'Commentaire',
        }


class DeleteReviewForm(forms.Form):
    """Formulaire pour la suppression de critique"""
    delete_review = forms.BooleanField(widget=forms.HiddenInput(), initial=True)


class SearchUserForm(forms.Form):
    """Formulaire pour la recherche d'utilisateurs"""
    username = forms.CharField(

        # Cacher affichage "username"
        label='',

        # Cacher affichage "Ce champ est obligatoire"
        error_messages={'required': ''},

        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Rechercher par nom'})
    )
