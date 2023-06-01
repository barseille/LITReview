from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.decorators import login_required
from . import models
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from itertools import chain
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.views import View
from django.core.exceptions import PermissionDenied




@login_required
def home(request):
    # users_followed = models.UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)

    # récupération de tous les tickets
    tickets = models.Ticket.objects.all().annotate(review_count=Count('review'))
    reviews = models.Review.objects.all()

    # lambda est un mot-clé en Python qui vous permet de déclarer des fonctions anonymes
    posts = sorted(
        chain(tickets, reviews), 
        key=lambda post: post.time_created, 
        reverse=True
    )

    return render(request, 'blog/home.html', context={'posts': posts})



#------------------------ticket--------------------

"""
LoginRequiredMixin : mixin qui s'assure que l'utilisateur est connecté 
avant de permettre l'accès à la vue.

CreateView est une vue générique basée sur une classe Django 
pour créer de nouvelles instances d'un modèle.
"""
class TicketCreateView(LoginRequiredMixin, CreateView):
    model = models.Ticket
    form_class = forms.TicketForm
    template_name = 'blog/create_ticket.html'
    success_url = reverse_lazy('home')

    """ 
    avant de sauvegarder l'objet Ticket, 
    on assigne l'utilisateur connecté actuellement  
    à l'attribut user du Ticket. 
    C'est pour cette raison qu'on surcharge la méthode form_valid.
    """
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def edit_ticket(request, ticket_id):
    
    # récupération de l'instance du ticket par son id
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    
    # Vérifiez si l'utilisateur connecté est celui qui a créé le ticket
    #  si utilisateur différent alors erreur 403 (interdiction)
    if ticket.user != request.user:
        raise PermissionDenied
    
    # Création d'un formulaire de modification prérempli avec les données du ticket existant
    edit_ticket = forms.TicketForm(instance=ticket)
    
    delete_ticket = forms.DeleteTicketForm()
    
    if request.method == 'POST':
        
        if 'edit_ticket' in request.POST:
            """
            Si le formulaire de modification est soumis, 
            il est re-créé avec les nouvelles données entrées par l'utilisateur
            """
            edit_ticket = forms.TicketForm(request.POST,request.FILES, instance=ticket)
            if edit_ticket.is_valid():
                edit_ticket.save()
                return redirect('home')
            
        if 'delete_ticket' in request.POST:
            delete_ticket = forms.DeleteTicketForm(request.POST)
            if delete_ticket.is_valid():
                ticket.delete()
                return redirect('home')
            
    else:
        # formulaires vides
        edit_ticket = forms.TicketForm(instance=ticket)
        delete_ticket = forms.DeleteTicketForm()
        
    # formulaires sont passés au template pour être affichés
    context = {
        'edit_ticket': edit_ticket,
        'delete_ticket': delete_ticket,
    }
    return render(request, 'blog/edit_ticket.html', context=context)

# ------------------------abonnement(subscribe)--------------


@login_required
def subscribe(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)

    # Liste des utilisateurs que l'utilisateur actuel suit déjà
    followed_users = models.UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)

    # Liste de tous les utilisateurs à l'exception de l'utilisateur actuel et ceux qu'il suit déjà
    all_users = get_user_model().objects.exclude(id__in=followed_users).exclude(id=request.user.id)

    # Liste des instances d'UserFollows où l'utilisateur actuel est le suiveur
    following = models.UserFollows.objects.filter(user=request.user)

    # Liste des instances d'UserFollows où l'utilisateur actuel est le suivi
    followers = models.UserFollows.objects.filter(followed_user=request.user)

    # Initialiser le formulaire de recherche
    search_form = forms.SearchUserForm(request.GET)
    searched_users = None

    if search_form.is_valid():
        searched_username = search_form.cleaned_data["username"]
        # Créer une nouvelle liste d'utilisateurs qui correspondent à la recherche
        searched_users = all_users.filter(username__icontains=searched_username)

    if request.method == "POST":
        user_to_follow = get_object_or_404(get_user_model(), id=request.POST.get('user_id'))
        try:
            if user_to_follow == request.user:
                raise ValidationError("Vous ne pouvez pas vous abonner à vous-même.")
            if user_to_follow in followed_users:
                raise ValidationError("Vous êtes déjà abonné à cet utilisateur.")
            models.UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
        except ValidationError as e:
            messages.error(request, e.message)

    context = {
        "user": user,
        "all_users": all_users,
        "followed_users": followed_users,
        "following": following,
        "followers": followers,
        "search_form": search_form,
        "searched_users": searched_users 
    }

    return render(request, "blog/subscribe.html", context=context)




@login_required
def unsubscribe(request, user_id):
    user_to_follow = get_object_or_404(get_user_model(), id=user_id)
    follow_object = models.UserFollows.objects.filter(user=request.user, followed_user=user_to_follow)
    
    if follow_object.exists():
        follow_object.delete()  
    return redirect("subscribe", user_id=request.user.id)


#-------------------critique(review)-------------

@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    form = forms.ReviewForm()

    if request.method == "POST":
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("home")
    else:
        form = forms.ReviewForm(initial={'ticket': ticket})
    return render(request, "blog/create_review.html", context={"form":form})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_review = forms.ReviewForm(instance=review)
    delete_review = forms.DeleteReviewForm()
    
    if request.method == "POST":
        if "edit_review" in request.POST:
            edit_review = forms.ReviewForm(request.POST, instance=review)
            if edit_review.is_valid():
                edit_review.save()
                return redirect("home")
        else:
            print(edit_review.errors)
        if "delete_review" in request.POST:
            delete_review = forms.DeleteReviewForm(request.POST)
            if delete_review.is_valid():
                review.delete()
                return redirect("home")
    else:
        edit_review = forms.ReviewForm(instance=review)
        delete_review = forms.DeleteReviewForm()
        
    context = {
        "edit_review": edit_review,
        "delete_review": delete_review,
    }
    return render(request, "blog/edit_review.html", context=context)


# ----------------------ticket avec critique-------------------------------------------

class CreateTicketAndReview(LoginRequiredMixin, View):
    template_name = 'blog/create_ticket_and_review.html'

    def get(self, request, *args, **kwargs):
        form_ticket = forms.TicketForm() 
        form_review = forms.ReviewForm() 
        return render(request, self.template_name, {'form_ticket': form_ticket, 'form_review': form_review})

    def post(self, request, *args, **kwargs):
        form_ticket = forms.TicketForm(request.POST, request.FILES) 
        form_review = forms.ReviewForm(request.POST) 
        if form_ticket.is_valid() and form_review.is_valid():
            ticket = form_ticket.save(commit=False)
            ticket.user = self.request.user
            ticket.save()

            review = form_review.save(commit=False)
            review.user = self.request.user
            review.ticket = ticket
            review.save()

            return redirect('home') 
        return render(request, self.template_name, {'form_ticket': form_ticket, 'form_review': form_review})
    
# ----------------------------------mes posts----------------------------------------------------

@login_required
def my_posts(request):
    # Récupérer les Tickets et les Reviews de l'utilisateur connecté
    tickets = models.Ticket.objects.filter(user=request.user).annotate(review_count=Count('review'))
    reviews = models.Review.objects.filter(user=request.user)

    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'blog/my_posts.html', context={'posts': posts})


