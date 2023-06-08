from django.contrib import admin
from django.urls import path
from authentication.views import LoginPageView
from authentication.views import SignupPageView
import authentication.views
import blog.views
from django.conf import settings
from django.conf.urls.static import static
from blog.views import TicketCreateView
from blog.views import CreateTicketAndReview


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginPageView.as_view(), name='login'),
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('home/', blog.views.home, name='home'),
    path('blog/create_ticket/', TicketCreateView.as_view(), name='create_ticket'),
    path('blog/<int:ticket_id>/edit_ticket', blog.views.edit_ticket, name='edit_ticket'),
    path("subscribe/", blog.views.subscribe, name="subscribe"),
    path('unsubscribe/', blog.views.unsubscribe, name='unsubscribe'),
    path('create_review/<int:ticket_id>/', blog.views.create_review, name='create_review'),
    path('blog/<int:review_id>/edit_review/', blog.views.edit_review, name="edit_review"),
    path('blog/create_ticket_and_review/', CreateTicketAndReview.as_view(), name='create_ticket_and_review'),
    path('my_posts/', blog.views.my_posts, name="my_posts"),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
