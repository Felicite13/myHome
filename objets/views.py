from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ObjetConnecte, Interaction
from django.utils.timezone import now
from .models import Piece

@login_required
def maison_view(request):
    pieces = Piece.objects.all()
    return render(request, 'maison.html', {'pieces': pieces})

@login_required
def voir_piece(request, id):
    piece = get_object_or_404(Piece, id=id)
    user = request.user

    if user.niveau not in ["intermédiaire", "avancé", "expert"]:
        return render(request, 'erreur.html', {'message': "Accès réservé à partir du niveau intermédiaire."})

    objets = piece.objets.all()

    if user.age and user.age < 15:
        objets = objets.exclude(restreint_enfant=True)
    if user.type_membre != "parent":
        objets = objets.exclude(controle_parent_uniquement=True)

    return render(request, 'voir_piece.html', {'piece': piece, 'objets': objets})


@login_required
def voir_objet(request, id):
    objet = get_object_or_404(ObjetConnecte, id=id)
    user = request.user

    # Début de la fonction
    if user.niveau not in ["intermédiaire", "avancé", "expert"]:
        return render(request, 'erreur.html', {'message': "Accès aux objets réservé à partir du niveau intermédiaire."})


    if user.age and user.age < 15 and objet.restreint_enfant:
        return render(request, 'erreur.html', {'message': "Accès interdit (objet restreint aux enfants)."})
    if user.type_membre != "parent" and objet.controle_parent_uniquement:
        return render(request, 'erreur.html', {'message': "Accès réservé aux parents."})

    if request.method == "POST":
        if user.niveau in["avancé", "expert"]:
            objet.etat = request.POST.get("etat") or objet.etat
            objet.intensite = request.POST.get("intensite") or objet.intensite
            objet.couleur = request.POST.get("couleur") or objet.couleur
            objet.volume = request.POST.get("volume") or objet.volume
            objet.musique = request.POST.get("musique") or objet.musique
            objet.temperature = request.POST.get("temperature") or objet.temperature
            objet.mode = request.POST.get("mode") or objet.mode
            objet.position = request.POST.get("position") or objet.position
            objet.consommation_eau = request.POST.get("consommation_eau") or objet.consommation_eau
            objet.date_derniere_interaction = now()
            objet.save()

        Interaction.objects.create(
            utilisateur=user,
            objet=objet,
            action=f"modification : {objet.nom}",
            points_gagnes=1.0
        )

        user.points += 1.0
        if user.points >= 7:
            user.niveau = "expert"
        elif user.points >= 5:
            user.niveau = "avancé"
        elif user.points >= 3:
            user.niveau = "intermédiaire"
        else:
            user.niveau = "débutant"
        user.save()

    return render(request, 'objet.html', {'objet': objet})

from django.contrib import messages
from django.http import HttpResponseForbidden

@login_required
def ajouter_objet_piece(request, piece_id):
    if request.user.niveau != "expert":
        return HttpResponseForbidden("Accès réservé aux experts.")

    piece = get_object_or_404(Piece, id=piece_id)

    if request.method == "POST":
        ObjetConnecte.objects.create(
            nom=request.POST.get("nom"),
            type_objet=request.POST.get("type_objet") or "autre",
            etat=request.POST.get("etat"),
            piece=piece,
            intensite=request.POST.get("intensite") or None,
            couleur=request.POST.get("couleur") or None,
            volume=request.POST.get("volume") or None,
            musique=request.POST.get("musique") or None,
            temperature=request.POST.get("temperature") or None,
            mode=request.POST.get("mode") or None,
            position=request.POST.get("position") or None,
            consommation_eau=request.POST.get("consommation_eau") or None,
        )
        messages.success(request, "Objet ajouté avec succès.")
        return redirect('voir_piece', id=piece.id)

    return render(request, 'ajouter_objet_piece.html', {'piece': piece})

@login_required
def supprimer_objet(request, id):
    objet = get_object_or_404(ObjetConnecte, id=id)
    
    if request.user.niveau == "expert":
        id_piece = objet.piece.id
        objet.delete()
        return redirect('voir_piece', id=id_piece)
    
    return redirect('maison')

from django.db.models import Count


def accueil_view(request):
    objets = ObjetConnecte.objects.all()

    nom_recherche = request.GET.get('recherche')
    type_filtre = request.GET.get('type')

    if nom_recherche:
        objets = objets.filter(nom__icontains=nom_recherche)
    if type_filtre:
        objets = objets.filter(type_objet=type_filtre)

    types_disponibles = ObjetConnecte.objects.values_list('type_objet', flat=True).distinct()

    return render(request, 'accueil.html', {
        'objets': objets,
        'types': types_disponibles
    })

@login_required
def statistiques_view(request):
    user = request.user
    if user.niveau not in ["avancé", "expert"]:
        return redirect('maison')

    stats = []

    for piece in Piece.objects.all():
        nb_objets = piece.objets.count()
        nb_interactions = Interaction.objects.filter(objet__piece=piece).count()
        stats.append({
            'piece': piece.nom,
            'nb_objets': nb_objets,
            'nb_interactions': nb_interactions
        })

    return render(request, 'statistiques.html', {'stats': stats})