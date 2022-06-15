import datetime
import json
from pathlib import PureWindowsPath
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import *
from .form import ExperienceForm
from .models import Classe, Defaut, Experience, Groupe, Sous_groupe

"""
    FONCTIONS UTILISABLE PAR LES VUES

    sépare chaque texte comportant des tirées pour facilité l'affichage dans la vue
    :param modelObject: requete base de donnée avec toute les données selectionnées
    :param lib_object: nom de l'attribut voulant être afficher
    :returns : tableau de string
"""


def afficherTiret(modelObject, lib_object):
    tab = []
    first_string = ''
    tmp = False
    tmp1 = False
    for i in modelObject[lib_object]:
        if tmp == True:
            first_string += '-'
            tmp = False
        else:
            pass

        if i == '-':
            tmp1 = True
        # vérifie que le char après le tiret est un espace
        elif tmp1 == True:
            if(i == ' '):
                tab.append(first_string)
                first_string = ''
                tmp = True
            else:
                first_string += ' '
                first_string += i
                tmp1 = False
        else:
            first_string += i

    tab.append(first_string)
    return tab


"""
    AFFICHAGE DES VUES
"""


def home(request):
    """
    Cette page est la page d' accueil du site, elle contient :
    """
    latest_experience_list = Experience.objects.order_by(
        '-experience_pub_date')[:5]
    context = {'latest_experience_list': latest_experience_list}
    return render(request, 'Webfautheque/home.html', context)


def page_arborescence_defautheque(request):
    """
    Cette page affiche les différentes Classes existante dans l' arborescence de la défauthèque,
    il s' agit des choix les plus haut (A, B, C ..., G)
    """
    classes_list = Classe.objects.all()
    context = {'classes_list': classes_list, }

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
    classe_idperso = Classe.objects.filter(classe_idperso=classe_idperso).values()[0]["classe_idperso"]
    context = {'sous_groupes_list': sous_groupes_list, 'classe_idperso' : classe_idperso}
    return render(request, 'Webfautheque/sous_groupes.html', context)


def page_defauts_defautheque(request, classe_idperso, groupe_idperso_one_char, sous_groupe_idperso_one_char):
    """
    Il s' agit de la page affichant les différents défauts contenu dans le sous groupe demandé.
    Il s' agit des choix juste après les sous-groupes.

    """
    # liste des défauts appartenant au sous_groupe qui correspond (sous_groupe_id_perso_one_char)
    defauts_list = Defaut.objects.filter(
        sous_groupe=Sous_groupe.objects.filter(
            sous_groupe_idperso=classe_idperso + groupe_idperso_one_char + sous_groupe_idperso_one_char + '0').values()[0]["id"])
        
    groupe_idperso = Groupe.objects.filter(groupe_idperso=classe_idperso + groupe_idperso_one_char + '00').values()[0]["groupe_idperso"]
    context = {'defauts_list': defauts_list, 'groupe_idperso': groupe_idperso}
    return render(request, 'Webfautheque/liste_defauts_sous_groupe.html', context)


def pages_defauts_liste(request):
    """
    Cette page affiche la liste des défauts existants dans la défauthèque.
    """
    defauts_list = Defaut.objects.all()
    context = {'defauts_list': defauts_list}
    return render(request, 'Webfautheque/liste_defauts.html', context)


def page_presentation_defaut(request, defaut_idperso):
    """
    Il s' agit de la page regroupant les causes, remèdes et description d'un défaut particulier.
    On y trouve un lien vers les expériences ainsi que les ift et rapport d'anomalie associé.
    """
    defaut_carac = Defaut.objects.filter(
        defaut_idperso=defaut_idperso).values()[0]
    idperso = defaut_carac['defaut_idperso']
    nom = defaut_carac['defaut_nom']
    remedes = afficherTiret(defaut_carac, 'defaut_remedes')
    causes = afficherTiret(defaut_carac, 'defaut_causes')
    infos = afficherTiret(defaut_carac, 'defaut_info')
    desc = afficherTiret(defaut_carac, 'defaut_description')
    sous_groupe_id = Sous_groupe.objects.filter(id = defaut_carac['sous_groupe_id']).values()[0]['sous_groupe_idperso']
    context = {'defaut_idperso': idperso, 'defaut_nom': nom, 'defaut_remedes': remedes,
               'defaut_causes': causes, 'defaut_infos': infos, 'defaut_description': desc, 'defaut_sous_groupe' : sous_groupe_id}
    return render(request, 'Webfautheque/description_defaut.html', context)


def page_choix_experience(request, defaut_idperso):
    """
    Il s' agit de la page listant les expériences d'un défaut sous forme d'un tableau, elle permet d'accèder à une expérience particulière.
    """
    experiences = Experience.objects.filter(
        defaut_id=Defaut.objects.filter(defaut_idperso=defaut_idperso).values()[0]["id"]).order_by('-experience_pub_date')
    paginator = Paginator(experiences, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    tags = Experience.objects.all().values('experience_auteur').distinct()
    groupes = request.user.groups.all()

    context = {'experiences': experiences, "defaut_idperso": defaut_idperso,
               'page_obj': page_obj, 'tags': tags, 'paginator': paginator, 'groupes': groupes}
    return render(request, 'Webfautheque/choix_experiences.html', context)


def page_consultation_experience(request, defaut_idperso, experience_id):
    """
    Il s'agit de la page affichant les informations d'une expérience particulière.
    """
    try:
        experience = Experience.objects.get(id=experience_id)
        experience = Experience.objects.filter(id=experience_id).values()[0]
        descriptif = afficherTiret(experience, 'experience_descriptif')
        remedes = afficherTiret(experience, 'experience_remedes')
        defaut_nom = Defaut.objects.filter(id=experience['defaut_id']).values()[
            0]['defaut_nom']
        pa = PureWindowsPath(experience['experience_rapport_anomalie'])
        context = {'experience': experience,
                   "defaut_nom": defaut_nom, "defaut_idperso": defaut_idperso, 'descriptif': descriptif, 'remedes': remedes, 'chemin_image': pa}
        return render(request, 'Webfautheque/consultation_experience.html', context)

    except:
        return redirect('page_choix_experience', defaut_idperso)


@permission_required('Webfautheque.add_experience')
def page_ajout_experience(request, defaut_idperso=''):
    """
    Il s'agit de la page permettant d'ajouter une expérience à un défaut.

    """
    # ajout d'un formulaire Expérience
    try:
        form = ExperienceForm()

        # Si Envoie formulaire :
        if request.method == 'POST':
            form = ExperienceForm(request.POST, request.FILES or None)
            if form.is_valid():

                # date non naive à la date du jour
                naive_datetime = datetime.datetime.now()
                naive_datetime.tzinfo  # None
                settings.TIME_ZONE  # 'UTC'

                experience = form.save(commit=False)

                experience.defaut_id = request.POST.get('defaut')
                experience.experience_pub_date = naive_datetime
                experience.save()

                return redirect('experience_list')

        # Affichage de la page quand ce n'est pas l'envoie du formulaire
        else:
            form = ExperienceForm(initial={
                                  'experience_auteur': request.user, 'experience_pub_date': datetime.datetime.now()})
            page = request.GET.get('page', 1)

            if(page == 'ajout_list'):
                defaut_nom = Defaut.objects.all()
                return render(request, 'Webfautheque/experience_ajout.html', {'experience_form': form, 'liste_defaut': defaut_nom})
            else:
                form.fields['defaut'].queryset = Defaut.objects.filter(
                    defaut_idperso=defaut_idperso)
                form.fields['defaut'].label = "Défaut"
                form.fields['defaut'].empty_label = None

                liste_defaut = Defaut.objects.all()
                defaut_nom = Defaut.objects.get(
                    defaut_idperso=defaut_idperso).defaut_nom
                defaut_id = Defaut.objects.get(
                    defaut_idperso=defaut_idperso).id

                return render(request, 'Webfautheque/experience_ajout.html', {'experience_form': form, 'defaut': defaut_idperso, 'nom_defaut': defaut_nom, 'defaut_id': defaut_id, 'liste_defaut': liste_defaut})
    except:
        return redirect('page_choix_experience', defaut_idperso)


@permission_required('Webfautheque.change_experience', login_url='/login/')
def page_update_experience(request, id, experience_id):
    """
    Page permettant de modifier une expérience via un formulaire.
    """
    try:
        form = ExperienceForm(request.POST)

        obj = get_object_or_404(Experience, id=experience_id)
        form = ExperienceForm(request.POST or None,
                              request.FILES or None, instance=obj,
                              initial={'experience_pub_date': datetime.datetime.now()})
        # Si Envoie formulaire :
        if form.is_valid():
            form.instance.experience_pub_date = datetime.datetime.now().replace(microsecond=0)
            form.save()

            return redirect('experience_list')
        # Affichage de la page quand ce n'est pas l'envoie du formulaire
        else:
            nom_exp = Experience.objects.get(
                id=experience_id).experience_nom_article
            liste_defaut = Defaut.objects.all()
            defaut_nom = Defaut.objects.get(defaut_idperso=id).defaut_nom
            defaut_id = Defaut.objects.get(defaut_idperso=id).id
            id_defaut = Defaut.objects.get(id=Experience.objects.get(
                id=experience_id).defaut_id).defaut_idperso
            return render(request, 'Webfautheque/experience_update.html', {'experience_form': form, 'experience_id': experience_id, 'nom_exp': nom_exp, 'id_defaut': id_defaut, 'liste_defaut': liste_defaut, 'nom_defaut': defaut_nom, 'defaut_id': defaut_id})

    except:
        return redirect('experience_list')


def experience_list(request):
    """
    Page affichant la liste des expériences.
    """
    experiences = Experience.objects.all().order_by('-experience_pub_date')
    paginator = Paginator(experiences, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    tags = Experience.objects.all().values('experience_auteur').distinct()
    groupes = request.user.groups.all()
    defauts = Defaut.objects.all()
    context = {'experiences': experiences, 'page_obj': page_obj,
               'tags': tags, 'paginator': paginator, 'groupes': groupes, 'defauts': defauts}
    return render(request, 'Webfautheque/experience_list.html', context)


@permission_required('Webfautheque.delete_experience', login_url='/login/')
@csrf_exempt
def page_delete_experience(request, id, experience_id):
    """
    Page permettant de supprimer une expérience.
    """
    try:
        experience = get_object_or_404(Experience, id=experience_id)
        if request.method == "POST":
            experience.delete()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        return render(request, 'Webfautheque/experience_list.html')
    except:
        return redirect('experience_list')


def login_user(request):
    """
    Fonction permettant de se connecter.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #authentification avec la méthode de django.
        user = authenticate(request, username=username, password=password)
        #si l'authentification est bonne.
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'Webfautheque/login.html', {'error_message': 'Identifiants incorrects'})
    else:
        return render(request, 'Webfautheque/login.html')


@login_required(login_url='/')
def logout_user(request):
    """
    Fonction permettant de se déconnecter.
    """
    logout(request)
    return redirect('/')


def search_experiences(request):
    """
    Filtre de recherche dans la liste des expériences.
    Filtre par Nom.
    """
    if request.method == 'POST':
        if(json.loads(request.body).get('searchValue') == None):
            search = ''
        else:
            search = json.loads(request.body).get('searchValue')
        experiences = Experience.objects.filter(
            experience_nom_article__icontains=search).order_by('-experience_pub_date')
        data = experiences.values()
        for experience in data:
            experience['defaut_nom'] = Defaut.objects.get(
                id=experience['defaut_id']).defaut_idperso

        return JsonResponse(list(data), safe=False,)


def search_experiences_by_defaut(request, defaut_idperso):
    """
    Filtre de recherche dans la liste des expériences.
    Filtre par Nom.
    """
    data = []
    if request.method == 'POST':
        search = json.loads(request.body).get('searchValue')
        iddefaut = Defaut.objects.get(defaut_idperso=defaut_idperso)
        experiences = Experience.objects.filter(
            experience_nom_article__icontains=search, defaut_id=iddefaut).order_by('-experience_pub_date')
        data = experiences.values()
        for experience in data:
            experience['defaut_nom'] = Defaut.objects.get(
                id=experience['defaut_id']).defaut_idperso
        return JsonResponse(list(data), safe=False,)


def experienceByAuteur(request):
    """
    Filtre de recherche dans la liste des expériences.
    Filtre par Auteur .
    """
    if request.method == 'POST':
        search = json.loads(request.body).get('name')
        experiences = Experience.objects.filter(
            experience_auteur=search).order_by('-experience_pub_date')
        data = experiences.values()
        for experience in data:
            experience['defaut_nom'] = Defaut.objects.get(
                id=experience['defaut_id']).defaut_idperso
        return JsonResponse(list(data), safe=False,)


def experienceAuteurDefaut(request, defaut_idperso):
    """
    Filtre de recherche dans un défaut spécifique.
    Filtre par Auteur.
    """
    data = []
    if request.method == 'POST':
        search = json.loads(request.body).get('name')
        iddefaut = Defaut.objects.get(defaut_idperso=defaut_idperso)
        experiences = Experience.objects.filter(
            experience_auteur=search, defaut_id=iddefaut).order_by('-experience_pub_date')
        data = experiences.values()
        for experience in data:
            experience['defaut_nom'] = Defaut.objects.get(
                id=experience['defaut_id']).defaut_idperso
        return JsonResponse(list(data), safe=False,)


def experienceByDefaut(request):
    """
    Filtre de recherche dans la liste des expériences.
    Filtre par Defaut.
    """
    if request.method == 'POST':
        search = json.loads(request.body).get('name')
        idDefaut = Defaut.objects.filter(
            defaut_idperso__icontains=search).order_by('-defaut_idperso')
        for defaut in idDefaut:
            experiences = Experience.objects.filter(
                defaut_id=defaut.id).order_by('-experience_pub_date')
            data = experiences.values()
            for experience in data:
                experience['defaut_nom'] = Defaut.objects.get(
                    id=experience['defaut_id']).defaut_idperso
        return JsonResponse(list(data), safe=False,)
