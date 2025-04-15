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
    
    def mettre_a_jour_niveau(self):
        if self.points >= 7:
            self.niveau = "expert"
        elif self.points >= 5:
            self.niveau = "avancé"
        elif self.points >= 3:
            self.niveau = "intermédiaire"
        else:
            self.niveau = "debutant"
        self.save()



