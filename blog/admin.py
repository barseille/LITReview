from django.contrib import admin
from .models import UserFollows


class UserFollowsAdmin(admin.ModelAdmin):

    # Ajout de champs dans l'administrateur Django
    list_display = ('user', 'followed_user')


admin.site.register(UserFollows, UserFollowsAdmin)
