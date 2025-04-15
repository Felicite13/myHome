from django.urls import path
from . import views
from .views import CustomLoginView
from .views import register_view, profil_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profil/', profil_view, name='profil'), 
    path('utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('utilisateur/<int:user_id>/interactions/', views.voir_interactions_utilisateur, name='voir_interactions_utilisateur'),
    path('regles/', views.regles_view, name='regles'),

 
]
