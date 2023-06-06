from django.conf import settings
from django.db import models
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator


class Ticket(models.Model):
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (400, 400)

    def resize_image(self):
        if self.image:
            image = Image.open(self.image.path)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refresh_from_db()
        self.resize_image()
        super().save(*args, **kwargs)


class UserFollows(models.Model):

    # utilisateur qui suit un autre utilisateur (ex : user=jean)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='following')

    # utilisateur qui est suivi par user (followed_user=bob, donc jean suit bob)
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='followers')

    class Meta:
        # un utilisateur ne peut suivre un autre utilisateur qu'une seule fois
        unique_together = ('user', 'followed_user')


class Review(models.Model):

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),
                                                          MaxValueValidator(5)])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
