# blog/models.py
from django.conf import settings
from django.db import models
from PIL import Image


class Ticket(models.Model):
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    
    
    IMAGE_MAX_SIZE = (800, 800)
    
    def resize_image(self):
        if self.image:
            image = Image.open(self.image.path)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.image.path)
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()
        
class UserFollows(models.Model):
    # utilisateur qui suit un autre utilisateur
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='suit')
    #  utilisateur qui est suivi
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='suivis_par')

    class Meta:
        # un utilisateur ne peut suivre un autre utilisateur qu'une seule fois
        unique_together = ('user', 'followed_user')
        
