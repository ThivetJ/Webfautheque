from django.contrib import admin

from .models import Classe, Groupe, Sous_groupe, Defaut, Experience

admin.site.register(Classe)
admin.site.register(Groupe)
admin.site.register(Sous_groupe)
admin.site.register(Defaut)
admin.site.register(Experience)
