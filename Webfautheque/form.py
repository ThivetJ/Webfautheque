from django import forms
from django.contrib import admin

from .models import Classe, Defaut, Experience, Groupe, Sous_groupe

# Formulaire Experience
class ExperienceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        self.fields['experience_auteur'].widget.attrs['readonly'] = True

    class Meta:
        model = Experience
        fields = ('defaut',
                  'experience_auteur',
                  'experience_nom_article',
                  'experience_descriptif',
                  'experience_pub_date',
                  'experience_remedes',
                  'experience_rapport_anomalie',
                  'experience_ift',
                  'experience_photos_1',
                  'experience_photos_2',
                  )
        widgets = {
            'experience_pub_date': forms.HiddenInput(),
            'experience_auteur': forms.HiddenInput(),
            'experience_ift': forms.HiddenInput(),
            'experience_ift': forms.FileInput(),
            'experience_rapport_anomalie': forms.FileInput(),
            'experience_photos_1': forms.HiddenInput(),
            'experience_photos_1': forms.FileInput(),
            'experience_photos_2': forms.HiddenInput(),
            'experience_photos_2': forms.FileInput(),
        }
