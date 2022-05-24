import datetime
import io
import json
import os
import random

from distutils.debug import DEBUG
from distutils.log import debug
from email import message
from email.policy import default
from fileinput import filename
from pickle import FALSE
from pydoc import describe
from tkinter import E
from xml.dom import NotFoundErr

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.http import FileResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import make_aware
from django.views.decorators.csrf import *
from faker import Faker
from requests import request

from .form import ExperienceForm
from .models import Classe, Defaut, Experience, Groupe, Sous_groupe

"""
    FONCTIONS UTILISABLE PAR LES VUES
"""

# insertion des groupes B200 à G200 dans la base de données
def insert_groupes():
    tab = ['B200', 'B300', 'C100', 'C200', 'C300', 'C400', 'D100',
           'D200', 'E100', 'E200', 'F100', 'F200', 'G100', 'G200']
    for i in tab:
        tab1 = i[0]
        cla_id = Classe.objects.filter(classe_idperso=tab1).values()[0]["id"]
        Groupe.objects.create(groupe_idperso=i, groupe_nom=i, classe_id=cla_id)

# insertion des sous_groupes de B220 à G260
def insert_sous_groupe():
    Sous_groupe.objects.create(
        sous_groupe_idperso='B120', sous_groupe_nom='B120', groupe_id=4)
    Sous_groupe.objects.create(
        sous_groupe_idperso='B210', sous_groupe_nom='B210', groupe_id=5)
    Sous_groupe.objects.create(
        sous_groupe_idperso='B220', sous_groupe_nom='B220', groupe_id=5)
    Sous_groupe.objects.create(
        sous_groupe_idperso='B310', sous_groupe_nom='B310', groupe_id=6)
    Sous_groupe.objects.create(
        sous_groupe_idperso='C110', sous_groupe_nom='C110', groupe_id=7)
    Sous_groupe.objects.create(
        sous_groupe_idperso='C120', sous_groupe_nom='C120', groupe_id=7)
    Sous_groupe.objects.create(
        sous_groupe_idperso='C210', sous_groupe_nom='C210', groupe_id=8)
    Sous_groupe.objects.create(
        sous_groupe_idperso='C220', sous_groupe_nom='C220', groupe_id=8)
    Sous_groupe.objects.create(
        sous_groupe_idperso='C310', sous_groupe_nom='C310', groupe_id=9)
    Sous_groupe.objects.create(
        sous_groupe_idperso='C320', sous_groupe_nom='C320', groupe_id=9)
    Sous_groupe.objects.create(
        sous_groupe_idperso='C330', sous_groupe_nom='C330', groupe_id=9)
    Sous_groupe.objects.create(
        sous_groupe_idperso='C410', sous_groupe_nom='C410', groupe_id=10)
    Sous_groupe.objects.create(
        sous_groupe_idperso='D110', sous_groupe_nom='D110', groupe_id=11)
    Sous_groupe.objects.create(
        sous_groupe_idperso='D120', sous_groupe_nom='D120', groupe_id=11)
    Sous_groupe.objects.create(
        sous_groupe_idperso='D130', sous_groupe_nom='D130', groupe_id=11)
    Sous_groupe.objects.create(
        sous_groupe_idperso='D140', sous_groupe_nom='D140', groupe_id=11)
    Sous_groupe.objects.create(
        sous_groupe_idperso='D210', sous_groupe_nom='D210', groupe_id=12)
    Sous_groupe.objects.create(
        sous_groupe_idperso='D220', sous_groupe_nom='D220', groupe_id=12)
    Sous_groupe.objects.create(
        sous_groupe_idperso='D230', sous_groupe_nom='D230', groupe_id=12)
    Sous_groupe.objects.create(
        sous_groupe_idperso='D240', sous_groupe_nom='D240', groupe_id=12)
    Sous_groupe.objects.create(
        sous_groupe_idperso='E110', sous_groupe_nom='E110', groupe_id=13)
    Sous_groupe.objects.create(
        sous_groupe_idperso='E120', sous_groupe_nom='E120', groupe_id=13)
    Sous_groupe.objects.create(
        sous_groupe_idperso='E210', sous_groupe_nom='E210', groupe_id=14)
    Sous_groupe.objects.create(
        sous_groupe_idperso='E220', sous_groupe_nom='E220', groupe_id=14)
    Sous_groupe.objects.create(
        sous_groupe_idperso='E230', sous_groupe_nom='E230', groupe_id=14)
    Sous_groupe.objects.create(
        sous_groupe_idperso='F110', sous_groupe_nom='F110', groupe_id=15)
    Sous_groupe.objects.create(
        sous_groupe_idperso='F120', sous_groupe_nom='F120', groupe_id=15)
    Sous_groupe.objects.create(
        sous_groupe_idperso='F210', sous_groupe_nom='F210', groupe_id=16)
    Sous_groupe.objects.create(
        sous_groupe_idperso='F220', sous_groupe_nom='F220', groupe_id=16)
    Sous_groupe.objects.create(
        sous_groupe_idperso='F230', sous_groupe_nom='F230', groupe_id=16)
    Sous_groupe.objects.create(
        sous_groupe_idperso='G110', sous_groupe_nom='G110', groupe_id=17)
    Sous_groupe.objects.create(
        sous_groupe_idperso='G120', sous_groupe_nom='G120', groupe_id=17)
    Sous_groupe.objects.create(
        sous_groupe_idperso='G130', sous_groupe_nom='G130', groupe_id=17)
    Sous_groupe.objects.create(
        sous_groupe_idperso='G140', sous_groupe_nom='G140', groupe_id=17)
    Sous_groupe.objects.create(
        sous_groupe_idperso='G210', sous_groupe_nom='G210', groupe_id=18)
    Sous_groupe.objects.create(
        sous_groupe_idperso='G220', sous_groupe_nom='G220', groupe_id=18)
    Sous_groupe.objects.create(
        sous_groupe_idperso='G260', sous_groupe_nom='G260', groupe_id=18)

# modification de la valeur 'sous_groupes' de la table défaut
# fonction permettant de classer tout les defauts dans le bon groupe
def update_defaut():
    allRecord = Defaut.objects.all().values('id').order_by('id')
    prec = Defaut.objects.filter(id=1).values('defaut_idperso').order_by('id')
    inc = 1
    t = 0
    for i in allRecord:
        if(Defaut.objects.filter(id=i['id']).values('defaut_idperso')[0]['defaut_idperso'][2] == prec[0]['defaut_idperso'][2]) and (Defaut.objects.filter(id=i['id']).values('defaut_idperso')[0]['defaut_idperso'][1] == prec[0]['defaut_idperso'][1]):
            prec = Defaut.objects.filter(id=i['id']).values(
                'defaut_idperso').order_by('id')
            Defaut.objects.filter(id=i['id']).update(sous_groupe_id=inc)
        else:
            prec = Defaut.objects.filter(id=i['id']).values(
                'defaut_idperso').order_by('id')
            inc += 1
            Defaut.objects.filter(id=i['id']).update(sous_groupe_id=inc)

# on appelle ces fonctions dans une vue pour ajouter les données dans la base



"""
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
    test = ''
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
    tab1 = []

    context = {'defauts_list': defauts_list}
    return render(request, 'Webfautheque/defaults.html', context)


def page_presentation_defaut(request, defaut_idperso):
    defaut_carac = Defaut.objects.filter(
        defaut_idperso=defaut_idperso).values()[0]
    idperso = defaut_carac['defaut_idperso']
    nom = defaut_carac['defaut_nom']
    remedes = afficherTiret(defaut_carac, 'defaut_remedes')
    causes = afficherTiret(defaut_carac, 'defaut_causes')
    infos = afficherTiret(defaut_carac, 'defaut_info')
    desc = afficherTiret(defaut_carac, 'defaut_description')

    context = {'defaut_idperso': idperso, 'defaut_nom': nom, 'defaut_remedes': remedes,
               'defaut_causes': causes, 'defaut_infos': infos, 'defaut_description': desc}
    return render(request, 'Webfautheque/defaut.html', context)


def page_choix_experience(request, defaut_idperso):
    experiences = Experience.objects.filter(
        defaut_id=Defaut.objects.filter(defaut_idperso=defaut_idperso).values()[0]["id"]).order_by('-experience_pub_date')
    paginator = Paginator(experiences, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    tags = Experience.objects.all().values('experience_auteur').distinct()
    groupes = request.user.groups.all()

    context = {'experiences': experiences, "defaut_idperso": defaut_idperso, 'page_obj': page_obj, 'tags': tags, 'paginator' : paginator, 'groupes' : groupes}
    return render(request, 'Webfautheque/choix_experiences.html', context)


def page_consultation_experience(request, defaut_idperso, experience_id):
    try:
        experience = Experience.objects.get(id=experience_id)
        experience = Experience.objects.filter(id=experience_id).values()[0]
        descriptif = afficherTiret(experience, 'experience_descriptif')
        remedes = afficherTiret(experience, 'experience_remedes')
        context = {'experience': experience,
                "defaut_idperso": defaut_idperso, 'descriptif': descriptif, 'remedes': remedes}
        return render(request, 'Webfautheque/consultation_experience.html', context)

    except :
        return redirect('page_choix_experience', defaut_idperso)


@permission_required('Webfautheque.add_experience')
def page_ajout_experience(request, defaut_idperso = ''):
    # ajout d'un formulaire Expérience
    try:
        form = ExperienceForm()

        #Si Envoie formulaire :  
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
            form = ExperienceForm(initial={ 'experience_auteur': request.user, 'experience_pub_date': datetime.datetime.now()})
            page = request.GET.get('page', 1)

            if(page == 'ajout_list'):
                defaut_nom = Defaut.objects.all()
                return render(request, 'Webfautheque/experience_ajout.html', {'experience_form': form, 'liste_defaut': defaut_nom})
            else:
                form.fields['defaut'].queryset = Defaut.objects.filter(defaut_idperso=defaut_idperso)
                form.fields['defaut'].label = "Défaut" 
                form.fields['defaut'].empty_label = None

                liste_defaut = Defaut.objects.all()
                defaut_nom = Defaut.objects.get(defaut_idperso=defaut_idperso).defaut_nom
                defaut_id = Defaut.objects.get(defaut_idperso=defaut_idperso).id
    
                return render(request, 'Webfautheque/experience_ajout.html', {'experience_form': form, 'defaut': defaut_idperso, 'nom_defaut': defaut_nom, 'defaut_id': defaut_id, 'liste_defaut': liste_defaut})
    except :
        return redirect('page_choix_experience', defaut_idperso)


@permission_required('Webfautheque.change_experience', login_url='/login/')
def page_update_experience(request, id, experience_id):
    try: 
        form = ExperienceForm(request.POST)
        
        obj = get_object_or_404(Experience, id=experience_id)
        form = ExperienceForm(request.POST or None,
                            request.FILES or None, instance=obj,
                            initial={'experience_pub_date': datetime.datetime.now()})

        if form.is_valid():
            form.instance.experience_pub_date = datetime.datetime.now().replace(microsecond=0)
            form.save()

            return redirect('experience_list')
        else:
            nom_exp = Experience.objects.get(id=experience_id).experience_nom_article
            liste_defaut = Defaut.objects.all()
            defaut_nom = Defaut.objects.get(defaut_idperso=id).defaut_nom
            defaut_id = Defaut.objects.get(defaut_idperso=id).id
            id_defaut = Defaut.objects.get(id=Experience.objects.get(id=experience_id).defaut_id).defaut_idperso
            return render(request, 'Webfautheque/experience_update.html', {'experience_form': form, 'experience_id': experience_id, 'nom_exp': nom_exp, 'id_defaut' : id_defaut, 'liste_defaut': liste_defaut, 'nom_defaut' : defaut_nom, 'defaut_id' : defaut_id})

    except :
        return redirect('experience_list')


def experience_list(request):
    experiences = Experience.objects.all().order_by('-experience_pub_date')
    paginator = Paginator(experiences, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    tags = Experience.objects.all().values('experience_auteur').distinct()
    groupes = request.user.groups.all()

    context = {'experiences': experiences, 'page_obj': page_obj, 'tags' : tags, 'paginator' : paginator, 'groupes' : groupes}
    return render(request, 'Webfautheque/experience_list.html', context)


@permission_required('Webfautheque.delete_experience', login_url='/login/')
@csrf_exempt
def page_delete_experience(request, id, experience_id):
    try: 
        context = {}    
        experience = get_object_or_404(Experience, id=experience_id)
        if request.method == "POST":
            experience.delete()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        return render(request, 'Webfautheque/experience_list.html', context)
    except:
        return redirect('experience_list')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'Webfautheque/login.html', {'error_message': 'Identifiants incorrects'})
    else:
        return render(request, 'Webfautheque/login.html')


@login_required(login_url='/')
def logout_user(request):
    logout(request)
    return redirect('/')
    

def search_experiences(request):
    if request.method =='POST':
        if(json.loads(request.body).get('searchValue')==None):
            search = ''
        else:
            search = json.loads(request.body).get('searchValue')
        experiences = Experience.objects.filter(experience_nom_article__icontains=search).order_by('-experience_pub_date')
        defaut = Defaut.objects.all()
        data = experiences.values()
        for experience in data:
            experience['defaut_nom'] = Defaut.objects.get(id=experience['defaut_id']).defaut_idperso
            
        return JsonResponse(list(data), safe=False,)


def search_experiences_by_defaut(request, defaut_idperso):
        data = []
        if request.method == 'POST':
            search = json.loads(request.body).get('searchValue')
            iddefaut = Defaut.objects.get(defaut_idperso = defaut_idperso)
            experiences = Experience.objects.filter(experience_nom_article__icontains=search, defaut_id = iddefaut).order_by('-experience_pub_date')
            data = experiences.values()
            for experience in data:
                experience['defaut_nom'] = Defaut.objects.get(id=experience['defaut_id']).defaut_idperso
            return JsonResponse(list(data), safe=False,)


def experienceByAuteur(request):
    if request.method =='POST':
        search = json.loads(request.body).get('name')
        experiences = Experience.objects.filter(experience_auteur=search).order_by('-experience_pub_date')
        data = experiences.values()
        for experience in data:
            experience['defaut_nom'] = Defaut.objects.get(id=experience['defaut_id']).defaut_idperso
        return JsonResponse(list(data), safe=False,)


def experienceAuteurDefaut(request, defaut_idperso):
        data = []
        if request.method == 'POST':
            search = json.loads(request.body).get('name')
            iddefaut = Defaut.objects.get(defaut_idperso = defaut_idperso)
            experiences = Experience.objects.filter(experience_auteur=search, defaut_id = iddefaut).order_by('-experience_pub_date')
            data = experiences.values()
            for experience in data:
                experience['defaut_nom'] = Defaut.objects.get(id=experience['defaut_id']).defaut_idperso
            return JsonResponse(list(data), safe=False,)


# ajout d'un jeu de données
# def fakerExperience(request):
#     fake = Faker()
#     for i in range(1, 100):

#         experience = Experience(experience_nom_article=fake.sentence(),
#                                 experience_descriptif=fake.text(),
#                                 experience_remedes=fake.text(),
#                                 experience_pub_date=datetime.datetime.now(),
#                                 experience_auteur=request.user,
#                                 defaut_id= random.randint(1, 100))
#         experience.save()
#     return redirect('experience_list')