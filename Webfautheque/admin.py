from gettext import ngettext
from django.contrib import admin
from django.forms import ChoiceField
from .models import *
from django.contrib import messages
from django.utils.translation import ngettext
from django.contrib.admin import AdminSite
import datetime


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
    list_display = ('groupe_idperso', 'groupe_nom', 'nom_classe')
    search_fields = ('groupe_nom',)
    list_filter = ('classe_id',)
    list_per_page = 10


@admin.register(Sous_groupe)
class Sous_groupeAdmin(admin.ModelAdmin):
    ordering = ('sous_groupe_idperso',)
    list_display = ('sous_groupe_idperso', 'sous_groupe_nom', 'nom_groupe')
    search_fields = ('sous_groupe_nom',)
    list_filter = ('groupe_id',)
    list_per_page = 10


@admin.register(Defaut)
class DefautAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('defaut_idperso', 'defaut_nom',
                    'defaut_description', '_sous_groupe')
    search_fields = ('defaut_nom',)
    list_filter = ('sous_groupe',)
    list_per_page = 10


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    ordering = ('-experience_pub_date',)
    list_display = ('nom_defaut', 'experience_nom_article', 'experience_descriptif',
                    'experience_remedes', 'experience_auteur', 'experience_pub_date')
    search_fields = ('experience_nom_article',)
    exclude = ('experience_pub_date',)
    list_filter = ('experience_pub_date', 'experience_auteur')
    date_hierarchy = 'experience_pub_date'
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        obj.experience_pub_date = datetime.datetime.now().replace(microsecond=0)
        obj.save()
    # ajoute l'auteur de l'experience dans l'interface admin
    def get_form(self, request, obj=None, **kwargs):
        if obj == "1":
            self.exclude = ("experience_auteur", )
        form = super(ExperienceAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['experience_auteur'].initial = request.user
        

        return form
    
        
    # desactiver une action
    # admin.site.disable_action('delete_selected')

    # ajout d'action dans l'interface admin
    #actions = ['exemple_action']

    @admin.action(description='exemple action')
    def exemple_action(self, request, queryset):
        updated = queryset.update(experience_descriptif='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Est ultricies integer quis auctor elit. A diam sollicitudin tempor id eu. Faucibus purus in massa tempor. Elementum sagittis vit')
        self.message_user(request, ngettext('%d message en cas de succes ', updated,)
                          % updated, messages.SUCESS)
