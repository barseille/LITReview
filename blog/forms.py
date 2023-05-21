# forms.py
from django import forms
from . import models
from django.contrib.auth import get_user_model

  
class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image'] 
            
class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
    
class SubscribeForm(forms.Form):
    user = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )   
    
class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], widget=forms.RadioSelect)
    
    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']
     

    
