from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.decorators import login_required
from . import models
from django.shortcuts import get_object_or_404


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'blog/home.html', context={'tickets': tickets})


@login_required
def create_ticket(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)  
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    context = {
        'ticket_form': ticket_form,
    }
    return render(request, 'blog/create_ticket.html', context=context)


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'blog/view_ticket.html', {'ticket': ticket})

@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_ticket = forms.TicketForm(instance=ticket)
    delete_ticket = forms.DeleteTicketForm()
    
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_ticket = forms.TicketForm(request.POST, instance=ticket)
            if edit_ticket.is_valid():
                edit_ticket.save()
                return redirect('home')
        if 'delete_ticket' in request.POST:
            delete_ticket = forms.DeleteTicketForm(request.POST)
            if delete_ticket.is_valid():
                ticket.delete()
                return redirect('home')
    context = {
        'edit_ticket': edit_ticket,
        'delete_ticket': delete_ticket,
    }
    return render(request, 'blog/edit_ticket.html', context=context)

# -----------------------abonnement---------------------------------------------

def subcribe(request):
    pass