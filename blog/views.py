from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from itertools import chain
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.views import View
from django.core.exceptions import PermissionDenied
from . import models
from . import forms


@login_required
def home(request):

    # récupération de tous les tickets
    tickets = models.Ticket.objects.all().annotate(review_count=Count('review'))
    reviews = models.Review.objects.all()

    """
    - lambda est un mot-clé en Python qui vous permet de déclarer des fonctions anonymes
    - liste unifier de tickets et de critiques triée par date du plus récent
    """
    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'blog/home.html', context={'posts': posts})


# ------------------------------ticket-----------------------------

"""
- LoginRequiredMixin : mixin qui s'assure que l'utilisateur est connecté
avant de permettre l'accès à la vue.

- CreateView : créez une instance d'un modèle à partir d'un formulaire.
"""


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = models.Ticket
    form_class = forms.TicketForm
    template_name = 'blog/create_ticket.html'
    success_url = reverse_lazy('home')

    """
    Avant de sauvegarder l'instance de Ticket qui est sur le point d'être créée,
    on assigne l'utilisateur actuellement connecté à son attribut user.
    C'est pour cette raison qu'on surcharge la méthode form_valid.
    """
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def edit_ticket(request, ticket_id):
    # récupération de l'instance du ticket par son id
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
 
    """
    Vérifiez si l'utilisateur connecté est celui qui a créé le ticket
    si utilisateur différent alors erreur 403 (interdiction)
    """
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
            edit_ticket = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if edit_ticket.is_valid():
                edit_ticket.save()
                return redirect('home')
            
        if 'delete_ticket' in request.POST:
            delete_ticket = forms.DeleteTicketForm(request.POST)
            if delete_ticket.is_valid():
                ticket.delete()
                return redirect('home')
        
    # formulaires sont passés au template pour être affichés
    context = {
        'edit_ticket': edit_ticket,
        'delete_ticket': delete_ticket,
    }
    return render(request, 'blog/edit_ticket.html', context=context)

# ------------------------abonnement(subscribe)---------------------


@login_required
def subscribe(request):
     
    # 'user' correspond à l'objet User de l'utilisateur dont l'id est passé dans l'URL.
    user = request.user

    # Liste des personnes que je suis
    following = request.user.following.all()
    
    #  Liste des personnes qui me suivent
    followers = request.user.followers.all()

    # Liste des personnes que je suis déjà
    followed_users_ids = following.values_list('followed_user', flat=True)

    # Liste de tous les utilisateurs à l'exception de l'utilisateur actuel et ceux qu'il suit déjà
    all_users = get_user_model().objects.exclude(id__in=followed_users_ids).exclude(id=request.user.id)

    # Initialiser le formulaire de recherche
    search_form = forms.SearchUserForm(request.GET)
    searched_users = None

    if search_form.is_valid():
        
        # extraire la valeur du champ username soumis par le formulaire
        searched_username = search_form.cleaned_data["username"]
        
        # Créer une nouvelle liste d'utilisateurs qui correspondent à la recherche
        searched_users = all_users.filter(username__icontains=searched_username)

    if request.method == "POST":
        user_to_follow = get_object_or_404(get_user_model(), id=request.POST.get('user_id'))
        try:
            if user_to_follow == request.user:
                raise ValidationError("Vous ne pouvez pas vous abonner à vous-même.")
            if user_to_follow.id in followed_users_ids:
                raise ValidationError("Vous êtes déjà abonné à cet utilisateur.")
            
            models.UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
            
        except ValidationError as error:
            messages.error(request, error.message)

    context = {
        
        "user": user,
        
        # liste de tous les utilisateurs que l'utilisateur actuel suit déjà
        "following": following,
        
        # liste de tous les utilisateurs qui suivent l'utilisateur actuel
        "followers": followers,
        
        # formulaire de recherche qui permet à l'utilisateur de chercher d'autres utilisateurs par nom
        "search_form": search_form,
        
        # liste de tous les utilisateurs qui correspondent a la recherche de l'utilisateur actuel
        "searched_users": searched_users
    }

    return render(request, "blog/subscribe.html", context=context)


@login_required
def unsubscribe(request):
    
    # récupération de l'ID de l'utilisateur à partir des données POST du formulaire
    user_id = request.POST.get('user_id')
    
    # récupération de l'utilisateur qu'on souhaite se désabonner
    user_to_follow = get_object_or_404(get_user_model(), id=user_id)
    
    # relation entre moi et l'utilisateur que je souhaite me déabonner
    follow_object = models.UserFollows.objects.filter(user=request.user, followed_user=user_to_follow)
    
    if follow_object.exists():
        follow_object.delete()
    
    # retour vers ma page "subscribe"
    return redirect("subscribe")


# -----------------------critique(review)--------------------------

@login_required
def create_review(request, ticket_id):
    
    # récupération du ticket à partir de la bdd en utilisant l'id fourni.
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    
    form = forms.ReviewForm()

    if request.method == "POST":
        form = forms.ReviewForm(request.POST)
        
        # si tous les champs requis sont présents
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("home")
    else:
        # formulaire vierge
        form = forms.ReviewForm()
    return render(request, "blog/create_review.html", context={"form": form})


@login_required
def edit_review(request, review_id):
    
    # récupération de l'objet Review avec "id" depuis la bdd
    review = get_object_or_404(models.Review, id=review_id)
    
    # récupération de l'instance du formulaire de critique avec les données
    edit_review = forms.ReviewForm(instance=review)
    
    delete_review = forms.DeleteReviewForm()
    
    if request.method == "POST":
        if "edit_review" in request.POST:
            edit_review = forms.ReviewForm(request.POST, instance=review)
            
            """
            si formulaire valide, les modifications sont enregistrées
            alors l'utilisateur sera redirigé vers le flux
            """
            if edit_review.is_valid():
                edit_review.save()
                return redirect("home")
    
        if "delete_review" in request.POST:
            delete_review = forms.DeleteReviewForm(request.POST)
            if delete_review.is_valid():
                review.delete()
                return redirect("home")
        
    context = {
        "edit_review": edit_review,
        "delete_review": delete_review,
    }
    return render(request, "blog/edit_review.html", context=context)


# ----------------------ticket avec critique------------------

class CreateTicketAndReview(LoginRequiredMixin, View):
    template_name = 'blog/create_ticket_and_review.html'

    def get(self, request):
        form_ticket = forms.TicketForm()
        form_review = forms.ReviewForm()
        context = {
            "form_ticket": form_ticket,
            "form_review": form_review,
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form_ticket = forms.TicketForm(request.POST, request.FILES)
        form_review = forms.ReviewForm(request.POST)
        
        if form_ticket.is_valid() and form_review.is_valid():
            
            # On enregistre le ticket sans le sauvegarder
            ticket = form_ticket.save(commit=False)
            
            # On ajoute l'utilisateur connecté comme auteur du ticket
            ticket.user = self.request.user
            
            # On sauvegarde maintenant le ticket dans la base de données
            ticket.save()

            review = form_review.save(commit=False)
            review.user = self.request.user
            
            # critique liée au ticket
            review.ticket = ticket
            review.save()
            context = {
                "form_ticket": form_ticket,
                "form_review": form_review,
            }
            return redirect('home')
        
        return render(request, self.template_name, context=context)
    
# -------------------mes posts---------------------


@login_required
def my_posts(request):
    
    # Récupérer les Tickets et les Reviews de l'utilisateur connecté
    tickets = models.Ticket.objects.filter(user=request.user).annotate(review_count=Count('review'))
    reviews = models.Review.objects.filter(user=request.user)

    # liste tickets et des critiques triées par date en ordre décroissant
    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'blog/my_posts.html', context={'posts': posts})
