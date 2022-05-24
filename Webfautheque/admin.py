import datetime
from importlib.resources import path
import os
from fileinput import filename
from gettext import ngettext
from pathlib import Path, PureWindowsPath, WindowsPath
from posixpath import dirname
from urllib.parse import urlencode

from django import forms, urls
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin import AdminSite
from django.forms import ChoiceField
from django.utils.translation import ngettext
from pymysql import STRING
from django.contrib.admin import SimpleListFilter

from Webfautheque.views import experience_list

from .models import *


class pageAdmin(AdminSite):
    AdminSite.site_header = 'Administration Webfautheque'
    AdminSite.index_title = 'page d\'administration'


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    ordering = ('classe_idperso',)
    list_display = ('classe_idperso', 'classe_nom')
    search_fields = ('classe_nom',)
    list_filter = ('classe_idperso',)
    list_per_page = 10


@admin.register(Groupe)
class GroupeAdmin(admin.ModelAdmin):
    ordering = ('groupe_idperso',)
    list_display = ('groupe_idperso', 'groupe_nom', "Classe")
    search_fields = ('classe',)
    list_filter = ('classe',)
    list_per_page = 10  

    #affichage du nom de la classe dans la liste des groupes 
    def Classe(self, obj):
        return obj.classe.classe_nom
    #affiche le nom de la classe en gardant l'id_perso de la classe en valeur 
    def get_form(self, request: object, obj: object, **kwargs: object) -> object:
        form = super(GroupeAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['classe'].choices = [(classe.id, classe.classe_nom) for classe in Classe.objects.all()]
        return form

@admin.register(Sous_groupe)
class Sous_groupeAdmin(admin.ModelAdmin):
    ordering = ('sous_groupe_idperso',)
    list_display = ('sous_groupe_idperso', 'sous_groupe_nom', 'nom_groupe')
    search_fields = ('sous_groupe_nom',)
    list_filter = ('groupe_id',)
    list_per_page = 10
    #affiche le nom du groupe en gardant l'id du sous groupe en valeur 
    def get_form(self, request: object, obj: object, **kwargs: object) -> object:
        form = super(Sous_groupeAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['groupe'].choices = [(groupe.id, groupe.groupe_nom) for groupe in Groupe.objects.all()]
        return form
    #affiche le nom du groupe dans la liste des sous groupes
    def nom_groupe(self, obj):
        return obj.groupe.groupe_nom

@admin.register(Defaut)
class DefautAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('defaut_idperso', 'defaut_nom',
                    'defaut_description', '_sous_groupe')
    search_fields = ('defaut_nom',)
    list_filter = ('sous_groupe',)
    list_per_page = 10
    #remplace la valeur du menu déroulant par le nom du sous groupe 
    def get_form(self, request: object, obj: object, **kwargs: object) -> object:
        form = super(DefautAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['sous_groupe'].choices = [(sous_groupe.id, sous_groupe.sous_groupe_nom) for sous_groupe in Sous_groupe.objects.all()]
        return form
    #affiche le nom du sous groupe dans la liste des défauts 
    def _sous_groupe(self, obj):
        return obj.sous_groupe.sous_groupe_nom

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    ordering = ('-experience_pub_date',)
    list_display = ('nom_defaut', 'experience_nom_article', 'experience_descriptif',
                    'experience_remedes', 'experience_auteur', 'experience_pub_date', 'experience_ift')
    search_fields = ('experience_nom_article',)
    exclude = ('experience_pub_date',)
    list_filter = ('experience_pub_date', 'experience_auteur')
    date_hierarchy = 'experience_pub_date'
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        obj.experience_pub_date = datetime.datetime.now().replace(microsecond=0)

        if obj.experience_ift:
            obj.experience_ift = obj.experience_ift
        obj.save()
    # ajoute l'auteur de l'experience dans l'interface admin
    def get_form(self, request, obj=None, **kwargs):
        form = super(ExperienceAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['defaut'].choices = [(defaut.id, defaut.defaut_nom) for defaut in Defaut.objects.all()]
        if obj == "1":
            self.exclude = ("experience_auteur", )
        if not obj:
            form.base_fields['experience_auteur'].initial = request.user.username
        else:
            form.base_fields['experience_auteur'].widget.attrs['readonly'] = True

        return form




    # desactiver une action
    # admin.site.disable_action('delete_selected')

    # ajout d'action dans l'interface admin
    # actions = ['exemple_action']

    @admin.action(description='exemple action')
    def exemple_action(self, request, queryset):
        updated = queryset.update(experience_descriptif='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Est ultricies integer quis auctor elit. A diam sollicitudin tempor id eu. Faucibus purus in massa tempor. Elementum sagittis vit')
        self.message_user(request, ngettext('%d message en cas de succes ', updated,)
                          % updated, messages.SUCESS)
