from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm

from django.core.mail import send_mail

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # ➕ Envoi de l’e-mail
            subject = "Bienvenue dans votre Maison Connectée !"
            message = f"Bonjour {user.username},\n\nVotre compte a bien été créé. Vous pouvez dès maintenant accéder à votre tableau de bord."
            from_email = None  # utilisera DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)

            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def profil_view(request):
    utilisateur = request.user
    return render(request, 'profil.html', {'utilisateur': utilisateur})

from django.contrib.auth.decorators import login_required
from users.models import User
from django.http import HttpResponseForbidden

@login_required
def liste_utilisateurs(request):
    if request.user.niveau != "expert":
        return HttpResponseForbidden("Accès réservé aux experts.")
    
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        nouveau_type = request.POST.get("type_membre")
        nouveau_niveau = request.POST.get("niveau")
        utilisateur = User.objects.get(id=user_id)
        utilisateur.type_membre = nouveau_type
        utilisateur.niveau = nouveau_niveau
        utilisateur.save()
    
    utilisateurs = User.objects.exclude(id=request.user.id)
    return render(request, 'liste_utilisateurs.html', {'utilisateurs': utilisateurs})

from objets.models import Interaction
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def voir_interactions_utilisateur(request, user_id):
    if request.user.niveau != "expert":
        return HttpResponseForbidden("Accès réservé aux experts.")

    utilisateur = User.objects.get(id=user_id)
    interactions = Interaction.objects.filter(utilisateur=utilisateur).order_by('-date')

    return render(request, 'interactions_utilisateur.html', {
        'utilisateur_cible': utilisateur,
        'interactions': interactions
    })


@login_required
def regles_view(request):
    return render(request, 'regles.html')