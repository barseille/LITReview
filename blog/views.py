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



@login_required
def home(request):
    # Liste des utilisateurs que l'utilisateur actuel suit
    users_followed = models.UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)

    tickets = models.Ticket.objects.filter(Q(user__in=users_followed) | Q(user=request.user))
    reviews = models.Review.objects.filter(Q(user__in=users_followed) | Q(ticket__user=request.user))

    posts = sorted(
        chain(tickets, reviews), 
        key=lambda post: post.time_created, 
        reverse=True
    )

    return render(request, 'blog/home.html', context={'posts': posts})


#------------------------ticket--------------------


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = models.Ticket
    form_class = forms.TicketForm
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
from .forms import SearchUserForm

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
    search_form = SearchUserForm(request.GET)
    searched_users = None

    if search_form.is_valid():
        searched_username = search_form.cleaned_data["username"]
        # Créer une nouvelle liste d'utilisateurs qui correspondent à la recherche
        searched_users = all_users.filter(username__icontains=searched_username)
        

    if request.method == "POST":
        user_to_follow = get_object_or_404(get_user_model(), id=request.POST.get('user_id'))
        if user_to_follow not in followed_users:
            models.UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
        else:
            models.UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).delete()

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


from django.views import View

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