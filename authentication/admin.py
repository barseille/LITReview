from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):    
    list_display = ('id', 'username', 'email', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('is_superuser', 'is_active')
    
admin.site.register(User, UserAdmin)
