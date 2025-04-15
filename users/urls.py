from django.urls import path
from . import views
from .views import CustomLoginView
from .views import register_view, profil_view
from django.conf import settings
from django.conf.urls.static import static
from .views import en_attente_validation
from .views import ma_famille_view
from .views import modifier_profil_view
from .views import fiche_utilisateur_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profil/', profil_view, name='profil'), 
    path('utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('utilisateur/<int:user_id>/interactions/', views.voir_interactions_utilisateur, name='voir_interactions_utilisateur'),
    path('regles/', views.regles_view, name='regles'),
    path('en-attente/', en_attente_validation, name='en_attente_validation'),
    path('modifier-profil/', modifier_profil_view, name='modifier_profil'),
    path('ma-famille/', ma_famille_view, name='ma_famille'),
    path('utilisateur/<int:user_id>/', fiche_utilisateur_view, name='fiche_utilisateur'),

 
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
