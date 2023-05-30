# forms.py
from django import forms
from . import models
from django.contrib.auth import get_user_model


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image'] 
        labels = {"title" : "Titre du ticket"}
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget = forms.FileInput() 
            
class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
    
class SubscribeForm(forms.Form):
    user = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )   
 

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], widget=forms.RadioSelect, label="Evalution")
    
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
        label='', 
        error_messages={
            'required': '', 
        },
        widget=forms.TextInput(attrs={'class': 'form-control', 
                                      'style': 'width:50%',
                                      'placeholder': 'Rechercher par nom'})
    )