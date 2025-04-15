from django.urls import path
from . import views
from .views import maison_view, voir_piece, voir_objet



urlpatterns = [
    path('maison/', maison_view, name='maison'),
    path('maison/piece/<int:id>/', voir_piece, name='voir_piece'),
    path('objet/<int:id>/', voir_objet, name='voir_objet'),
    path('piece/<int:piece_id>/ajouter/', views.ajouter_objet_piece, name='ajouter_objet_piece'),
    path('objet/<int:id>/supprimer/', views.supprimer_objet, name='supprimer_objet'),
    path('statistiques/', views.statistiques_view, name='statistiques'),
]
