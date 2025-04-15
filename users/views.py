from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from django.contrib import messages


from django.core.mail import send_mail

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # ❌ désactivé par défaut
            user.save()

            #  Générer un lien d’activation sécurisé
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(
                reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
            )

            #  Envoi du mail
            subject = "Activation de votre compte My Home"
            message = f"Bonjour {user.username},\n\nVeuillez cliquer sur ce lien pour activer votre compte :\n{activation_link}"
            send_mail(subject, message, None, [user.email])

            messages.success(request, "Un e-mail d’activation vous a été envoyé.")
            return render(request, 'confirmation_inscription.html')

    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def en_attente_validation(request):
    return render(request, 'en_attente_validation.html')



from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import redirect
from .models import User

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        if user:
            user.points += 0.25
            user.mettre_a_jour_niveau()
            user.save()
        login(self.request, user)
        return redirect(self.get_success_url())

from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404, HttpResponse

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'activation_succes.html')
    else:
        return HttpResponse("Lien d’activation invalide ou expiré.")



from .forms import UpdatePhotoForm

@login_required
def profil_view(request):
    utilisateur = request.user
    if not utilisateur.is_superuser and not utilisateur.est_valide:
        return render(request, 'en_attente_validation.html')
    form = UpdatePhotoForm(request.POST or None, request.FILES or None, instance=utilisateur)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profil')

    return render(request, 'profil.html', {'utilisateur': utilisateur, 'form': form})

@login_required
def modifier_profil_view(request):
    utilisateur = request.user
    form = RegisterForm(request.POST or None, request.FILES or None, instance=utilisateur)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Votre profil a bien été mis à jour.")
        return redirect('profil')

    return render(request, 'modifier_profil.html', {'form': form})



from django.contrib.auth.decorators import login_required
from users.models import User
from django.http import HttpResponseForbidden

from django.contrib import messages

@login_required
def ma_famille_view(request):
    if not request.user.est_valide:
        return redirect('en_attente_validation')

    membres = User.objects.exclude(id=request.user.id)
    return render(request, 'ma_famille.html', {'membres': membres})


@login_required
def liste_utilisateurs(request):
    if request.user.niveau != "expert":
        return HttpResponseForbidden("Accès réservé aux experts.")

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        utilisateur = User.objects.get(id=user_id)

        if "supprimer" in request.POST:
            if utilisateur == request.user:
                messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
            elif utilisateur.niveau == "expert":
                messages.error(request, "Vous ne pouvez pas supprimer un autre expert.")
            else:
                utilisateur.delete()
                messages.success(request, f"L'utilisateur {utilisateur.username} a été supprimé.")
            return redirect('liste_utilisateurs')

        elif "valider" in request.POST:
            utilisateur.est_valide = True
            utilisateur.save()
            messages.success(request, f"L'utilisateur {utilisateur.username} a été validé.")
            return redirect('liste_utilisateurs')

        # Mise à jour type/niveau
        nouveau_type = request.POST.get("type_membre")
        nouveau_niveau = request.POST.get("niveau")
        utilisateur.type_membre = nouveau_type
        utilisateur.niveau = nouveau_niveau
        utilisateur.save()
        messages.success(request, f"Le profil de {utilisateur.username} a été mis à jour.")
        return redirect('liste_utilisateurs')

    utilisateurs = User.objects.exclude(id=request.user.id)
    return render(request, 'liste_utilisateurs.html', {'utilisateurs': utilisateurs})




from objets.models import Interaction
from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from users.models import User

@login_required
def fiche_utilisateur_view(request, user_id):
    if request.user.niveau != 'expert':
        return HttpResponseForbidden("Accès réservé aux experts.")
    
    utilisateur = get_object_or_404(User, id=user_id)
    return render(request, 'fiche_utilisateur.html', {'utilisateur': utilisateur})


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