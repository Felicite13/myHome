# Generated by Django 5.2 on 2025-04-14 16:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ObjetConnecte",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                ("type_objet", models.CharField(max_length=50)),
                ("connectivite", models.CharField(blank=True, max_length=100)),
                (
                    "etat",
                    models.CharField(
                        choices=[
                            ("connecté", "connecté"),
                            ("déconnecté", "déconnecté"),
                        ],
                        default="connecté",
                        max_length=20,
                    ),
                ),
                ("marque", models.CharField(blank=True, max_length=50)),
                ("batterie", models.IntegerField(default=100)),
                ("date_derniere_interaction", models.DateTimeField(auto_now=True)),
                ("restreint_enfant", models.BooleanField(default=False)),
                ("controle_parent_uniquement", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Piece",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Interaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("action", models.CharField(max_length=50)),
                ("points_gagnes", models.FloatField(default=0)),
                (
                    "utilisateur",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "objet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="objets.objetconnecte",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="objetconnecte",
            name="piece",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="objets",
                to="objets.piece",
            ),
        ),
    ]
