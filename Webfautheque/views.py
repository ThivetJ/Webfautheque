from django.http import HttpResponse
from django.shortcuts import render

from .models import Classe, Groupe, Sous_groupe, Defaut, Experience


def home(request):
    """
    Cette page est la page d' accueil du site, elle contient :
    """
    latest_experience_list = Experience.objects.order_by('-experience_pub_date')[:5]
    context = {'latest_experience_list': latest_experience_list}
    return render(request, 'Webfautheque/home.html', context)


def page_arborescence_defautheque(request):
    """
    Cette page affiche les différentes Classes existante dans l' arborescence de la défauthèque,
    il s' agit des choix les plus haut (A, B, C ..., G)
    """
    classes_list = Classe.objects.all()
    context = {'classes_list': classes_list}
    return render(request, 'Webfautheque/arborescence.html', context)


def page_groupes_defautheque(request, classe_idperso):
    """
    Cette page affiche les différents Groupes existants dans la classe demandée,
     il s' agit des choix juste après les classes.
    """
    # liste de tous les groupes appartenant à la classe qui correspondant (class_idperso)
    groupes_list = Groupe.objects.filter(
        classe_id=Classe.objects.filter(classe_idperso=classe_idperso).values()[0]["id"])

    context = {'groupes_list': groupes_list}
    return render(request, 'Webfautheque/groupes.html', context)


def page_sous_groupes_defautheque(request, classe_idperso, groupe_idperso_one_char):
    """
    Cette page affiche les différents Sous-groupes existants dans le groupe demandé,
    il s' agit des choix juste après les groupes.
    """
    # liste de sous groupes appartenant au groupe qui correspond (groupe_idperso)
    sous_groupes_list = Sous_groupe.objects.filter(
        groupe_id=Groupe.objects.filter(groupe_idperso=classe_idperso + groupe_idperso_one_char + '00').values()[0][
            "id"])

    context = {'sous_groupes_list': sous_groupes_list}
    return render(request, 'Webfautheque/sous_groupes.html', context)


def page_defauts_defautheque(request, classe_idperso, groupe_idperso_one_char, sous_groupe_idperso_one_char):
    """
    Il s' agit de la page affichant les différents défauts contenu dans le sous groupe demandé.
    Il s' agit des choix juste après les sous-groupes.

    """
    # liste des défauts appartenant au sous_groupe qui correspond (sous_groupe_id_perso_one_char)
    defauts_list = Defaut.objects.filter(
        sous_groupe_id=Sous_groupe.objects.filter(
            sous_groupe_idperso=classe_idperso + groupe_idperso_one_char + sous_groupe_idperso_one_char + '0').values()[
            0]["id"])

    context = {'defauts_list': defauts_list}
    return render(request, 'Webfautheque/defauts.html', context)


def page_presentation_defaut(request, defaut_idperso):
    """
    Cette page est la page de présentation des défauts, elle affiche toutes les informations utile à la connaissance
    d' un défaut et à sa résolution.
    C'est à partir de cette page que l' on peut venir  :

        TODO : - demander une modification des informations affichées

    """
    defaut_carac = Defaut.objects.filter(defaut_idperso=defaut_idperso).values()[0]
    context = {'defauts_carac': defaut_carac}
    return render(request, 'Webfautheque/defaut.html', context)


def page_choix_experience(request, defaut_idperso):
    """
    Cette page répertorie l' ensemble des experiences associés à un défaut les affiches et propose :
        TODO : - d' ajouter une nouvelle expérience
    """
    experiences = Experience.objects.filter(
        defaut_id=Defaut.objects.filter(defaut_idperso=defaut_idperso).values()[0]["id"])
    context = {'experiences': experiences, "defaut_idperso": defaut_idperso}
    return render(request, 'Webfautheque/choix_experiences.html', context)


def page_consultation_experience(request, defaut_idperso, experience_id):
    """
    Cette page affiche une expérience lié à un défaut choisit dans la page page_choix_experience.
    Elle permet de :
        TODO : - mettre en avant l' expérience
        TODO : - proposer une modification de l' expérience

    """
    experience = Experience.objects.get(id=experience_id)
    context = {'experience': experience, "defaut_idperso": defaut_idperso}
    return render(request, 'Webfautheque/consultation_experience.html', context)


def page_ajout_experience(request, defaut_idperso):
    """
    Cette page permet de :
         TODO : - ajouter toutes les informations liés à une expérience (à définir)

    """
    return HttpResponse("Voici la page d' ajout d'une expérience pour le défaut {}".format(defaut_idperso))
