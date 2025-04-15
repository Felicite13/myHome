from django.db import models
from users.models import User

class Piece(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class ObjetConnecte(models.Model):
    nom = models.CharField(max_length=100)
    type_objet = models.CharField(max_length=100)
    etat = models.CharField(max_length=100, default="éteint")
    piece = models.ForeignKey(Piece, related_name="objets", on_delete=models.CASCADE)

    intensite = models.PositiveIntegerField(null=True, blank=True)  # lumière
    couleur = models.CharField(max_length=20, null=True, blank=True)

    volume = models.PositiveIntegerField(null=True, blank=True)  # enceinte
    musique = models.CharField(max_length=100, null=True, blank=True)

    temperature = models.FloatField(null=True, blank=True)  # thermostat, sèche-serviette
    mode = models.CharField(max_length=50, null=True, blank=True)  # thermostat, lit

    position = models.CharField(max_length=20, null=True, blank=True)  # volet, parasol, lit
    consommation_eau = models.FloatField(null=True, blank=True)  # capteur d'eau

    restreint_enfant = models.BooleanField(default=False)
    controle_parent_uniquement = models.BooleanField(default=False)

    date_derniere_interaction = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.type_objet})"





class Interaction(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    objet = models.ForeignKey(ObjetConnecte, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50)
    points_gagnes = models.FloatField(default=0)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.action} sur {self.objet.nom}"
