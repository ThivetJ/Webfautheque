from django import forms
from .models import Classe, Groupe, Sous_groupe, Defaut, Experience

# Formulaire Experience


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience

        # champs à afficher dans le formulaire
        fields = ('defaut',
                  'experience_auteur',
                  'experience_nom_article',
                  'experience_descriptif',
                  'experience_pub_date',
                  'experience_remedes',
                  'experience_rapport_anomalie',
                  'experience_ift',
                  'experience_photos',
                  )
        widgets = {
            
            'experience_pub_date': forms.HiddenInput(),
            'experience_ift': forms.HiddenInput(),
            'experience_ift': forms.FileInput(),
            'experience_rapport_anomalie': forms.HiddenInput(),
            'experience_rapport_anomalie': forms.FileInput(),
            'experience_photos': forms.HiddenInput(),
            'experience_photos': forms.FileInput(),
        }
