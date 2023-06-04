from django import forms
from . import models
from django.contrib.auth import get_user_model


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        labels = {"title": "Titre du ticket"}
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # forms.FileInput() : champ de saisi de fichier
        self.fields['image'].widget = forms.FileInput()
    
            
class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
    
class SubscribeForm(forms.Form):
    user = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class ReviewForm(forms.ModelForm):
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
    delete_review = forms.BooleanField(widget=forms.HiddenInput(), initial=True)


class SearchUserForm(forms.Form):
    username = forms.CharField(
        
        # cacher affichage "username"
        label='',
        
        # cacher affichage "Ce champ est obligatoire"
        error_messages={'required': ''},
        
        # form-control est une classe CSS fournie par Bootstrap
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Rechercher par nom'})
    )
