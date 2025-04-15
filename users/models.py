from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    type_membre = models.CharField(max_length=50, null=True, blank=True)
    niveau = models.CharField(max_length=15, default="débutant")
    points = models.FloatField(default=0.0)
    photo = models.ImageField(upload_to='photos_profil/', null=True, blank=True)  #

    def __str__(self):
        return self.username

