# url.py
from django.contrib import admin
from django.urls import path
import authentication.views
import blog.views
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
            template_name='authentication/login.html',
            redirect_authenticated_user=True),
        name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('home/', blog.views.home, name='home'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('blog/create_ticket', blog.views.create_ticket, name='create_ticket'),
    path('blog/<int:ticket_id>', blog.views.view_ticket, name='view_ticket'),
    path('blog/<int:ticket_id>/edit', blog.views.edit_ticket, name='edit_ticket'),
    path("subscribe/", blog.views.subscribe, name="subscribe"),
    path('unsubscribe/<int:user_id>/', blog.views.unsubscribe, name='unsubscribe'),
    path("profile/<int:user_id>/", blog.views.profile, name="profile"),
    path('create_review/<int:ticket_id>/', blog.views.create_review, name='create_review'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

