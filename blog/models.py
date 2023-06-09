from django.conf import settings
from django.db import models
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator


class Ticket(models.Model):
    """
    La classe Ticket représente les publications soumises par les utilisateurs.
    """
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (400, 400)

    def resize_image(self):
        """
        Surcharge la méthode save pour inclure le redimensionnement de l'image.

        La méthode fait les opérations suivantes :
        1. Sauvegarde l'objet Ticket dans la bdd avec l'image ajoutée.
        2. Rafraîchit l'objet depuis la bdd pour tenir compte des éventuelles modifications de l'image par le système.
        3. Redimensionne l'image si elle dépasse une taille maximale spécifiée.
        4. Sauvegarde à nouveau l'objet avec l'image redimensionnée.
        """
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
    """
    La classe UserFollows représente la relation de suivi entre les utilisateurs.
    """

    # C'est l'utilisateur qui suit d'autres utilisateurs.
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='following')

    # C'est l'utilisateur qui est suivi par d'autres utilisateurs.
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='followers')

    class Meta:
        # Un utilisateur ne peut suivre un autre utilisateur qu'une seule fois
        unique_together = ('user', 'followed_user')


class Review(models.Model):
    """
    La classe Review représente les critiques laissées par les utilisateurs.
    """

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),
                                                          MaxValueValidator(5)])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
