from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.decorators import login_required
from . import models
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from itertools import chain


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    posts = sorted(
        chain(tickets, reviews), 
        key=lambda post: post.time_created, 
        reverse=True
    )
    return render(request, 'blog/home.html', context={'posts': posts})

#------------------------ticket--------------------
# views.py
from django.views.generic import CreateView
from .forms import TicketForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = models.Ticket
    form_class = TicketForm
    template_name = 'blog/create_ticket.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_ticket = forms.TicketForm(instance=ticket)
    delete_ticket = forms.DeleteTicketForm()
    
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
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
        edit_ticket = forms.TicketForm(instance=ticket)
        delete_ticket = forms.DeleteTicketForm()
    context = {
        'edit_ticket': edit_ticket,
        'delete_ticket': delete_ticket,
    }
    return render(request, 'blog/edit_ticket.html', context=context)

# ------------------------abonnement(subscribe)--------------


@login_required
def subscribe(request):
    """ 
    Ici, nous récupérons la liste des utilisateurs que l'utilisateur connecté suit déjà.
    La méthode `values_list` renvoie une liste de tuples. L'argument `flat=True` rend la liste "plate",
    c'est-à-dire une simple liste d'IDs d'utilisateurs.
    """
    already_followed = models.UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)

    # Création d'une instance du formulaire SubscribeForm
    form = forms.SubscribeForm()

    """
    On modifie le champ "user" du formulaire pour exclure :
    - les utilisateurs que l'utilisateur connecté suit déjà (already_followed)
    - l'utilisateur connecté lui-même (request.user.id)
    """
    form.fields["user"].queryset = get_user_model().objects.exclude(id__in=already_followed).exclude(id=request.user.id)
    
    # Si la requête est de type POST (soumission du formulaire)
    if request.method == "POST":
        # On crée une nouvelle instance du formulaire avec les données envoyées par l'utilisateur
        form = forms.SubscribeForm(request.POST)

        # On applique la même logique d'exclusion pour le queryset du champ "user" du formulaire
        form.fields["user"].queryset = get_user_model().objects.exclude(id__in=already_followed).exclude(id=request.user.id)

        # On vérifie que les données envoyées par l'utilisateur sont valides
        if form.is_valid():
            # On récupère la liste des utilisateurs que l'utilisateur connecté veut suivre
            followed_users = form.cleaned_data["user"]
            for user in followed_users:
                # On vérifie si l'utilisateur connecté suit déjà l'utilisateur sélectionné
                exists = models.UserFollows.objects.filter(user=request.user, followed_user=user).exists()

                # Si ce n'est pas le cas, on crée une nouvelle instance de UserFollows
                if not exists:
                    models.UserFollows.objects.create(user=request.user, followed_user=user)

            # On redirige l'utilisateur vers la page d'accueil après la soumission du formulaire
            return redirect("home")
    
    # On crée un dictionnaire avec les données à envoyer au template
    context = {"subscribe_form": form}
    
    # On renvoie le template subscribe.html avec le contexte créé
    return render(request, "blog/subscribe.html", context=context)


@login_required
def unsubscribe(request, user_id):
    user_to_follow = get_object_or_404(get_user_model(), id=user_id)
    follow_object = models.UserFollows.objects.filter(user=request.user, followed_user=user_to_follow)
    
    if follow_object.exists():
        follow_object.delete()  
    return redirect("profile", user_id=request.user.id)


@login_required
def profile(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    following = models.UserFollows.objects.filter(user=user)
    followers = models.UserFollows.objects.filter(followed_user=user)
    
    context = {
        "user": user,
        "following": following,
        "followers":followers,
    }
    return render(request, "blog/profile.html", context=context)


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



# reviews = Review.objects.filter(
#         Q(user__in=users_followed) | Q(ticket__user=user))

# posts = sorted(chain(reviews, tickets),
#                    key=lambda post: post.time_created, reverse=True)