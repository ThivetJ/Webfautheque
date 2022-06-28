import datetime
from django import forms
from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import *
from django.contrib.admin.models import LogEntry


class pageAdmin(AdminSite):
    AdminSite.site_header = 'Administration Défauthèque'
    AdminSite.index_title = 'page d\'administration'
    AdminSite.site_title = 'Défauthèque'


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    list_display = ('object_repr', 'content_type',
                    'action_flag', 'user', 'action_time')
    list_filter = ['action_flag']
    search_fields = ['object_repr', 'change_message']
    list_per_page = 10
    readonly_fields = []


    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


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

    # affichage du nom de la classe dans la liste des groupes
    def Classe(self, obj):
        return obj.classe.classe_nom
        
    # affiche le nom de la classe en gardant l'id_perso de la classe en valeur
    def get_form(self, request: object, obj: object, **kwargs: object) -> object:
        form = super(GroupeAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['classe'].choices = [
            (classe.id, classe.classe_nom) for classe in Classe.objects.all()]
        return form


@admin.register(Sous_groupe)
class Sous_groupeAdmin(admin.ModelAdmin):
    ordering = ('sous_groupe_idperso',)
    list_display = ('sous_groupe_idperso', 'sous_groupe_nom', '_groupe')
    search_fields = ('sous_groupe_nom',)
    list_filter = ('groupe_id',)
    list_per_page = 10

    # affiche le nom du groupe en gardant l'id du sous groupe en valeur
    def get_form(self, request: object, obj: object, **kwargs: object) -> object:
        form = super(Sous_groupeAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['groupe'].choices = [
            (groupe.id, groupe.groupe_nom) for groupe in Groupe.objects.all()]
        return form

    # affiche le nom du groupe dans la liste des sous groupes
    def _groupe(self, obj):
        return obj.groupe.groupe_nom


@admin.register(Defaut)
class DefautAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('defaut_idperso', 'defaut_nom',
                    'defaut_description', '_sous_groupe')
    search_fields = ('defaut_nom',)
    list_filter = ('sous_groupe',)
    list_per_page = 10


    # remplace la valeur du menu déroulant par le nom du sous groupe
    def get_form(self, request: object, obj: object, **kwargs: object) -> object:
        form = super(DefautAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['sous_groupe'].choices = [
            (sous_groupe.id, sous_groupe.sous_groupe_nom) for sous_groupe in Sous_groupe.objects.all()]
        return form

    # affiche le nom du sous groupe dans la liste des défauts
    def _sous_groupe(self, obj):
        return obj.sous_groupe.sous_groupe_nom

    # permet de stocker l'image du defaut dans le repertoire associé à l'id du defaut
    def save_model(self, request, obj, form, change):
        # le nom du fichier doit être identique à l'id du defaut et avec un format png
        if obj.defaut_image:
            obj.defaut_image.name = obj.defaut_idperso + '/' + obj.defaut_image.name
        obj.save()


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    ordering = ('-experience_pub_date',)
    list_display = ('experience_nom_article', 'nom_defaut', 'experience_descriptif',
                    'experience_remedes', 'experience_auteur', 'experience_pub_date')
    search_fields = ('experience_nom_article',)
    exclude = ('experience_pub_date',)
    list_filter = ('experience_pub_date', 'experience_auteur')
    date_hierarchy = 'experience_pub_date'
    list_per_page = 10

    # lors de la sauvegarde d'une experience, ajoute la date actuelle sans les milisecondes
    def save_model(self, request, obj, form, change):
        obj.experience_pub_date = datetime.datetime.now().replace(microsecond=0)
        obj.save()

    # ajoute les différents éléments dans la base lors de la création ou modification d'une experience
    def get_form(self, request, obj=None, **kwargs):
        form = super(ExperienceAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['defaut'].choices = [
            (defaut.id, defaut.defaut_nom) for defaut in Defaut.objects.all()]
        form.base_fields['experience_rapport_anomalie'].widget = forms.FileInput()
        form.base_fields['experience_ift'].widget = forms.FileInput()

        # 1 = experience est modifiée, on initialise les champs auteur, rapport anomalie et ift avec la valeur déjà existante
        if obj == "1":
            self.exclude = ("experience_auteur", )
            form.base_fields['experience_rapport_anomalie'].initial = obj.experience_rapport_anomalie
            form.base_fields['experience_ift'].initial = obj.experience_ift
        if not obj:
            form.base_fields['experience_auteur'].initial = request.user.username

        else:
            form.base_fields['experience_auteur'].widget.attrs['readonly'] = True

        return form