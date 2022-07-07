from django import forms
from .models import Defaut, Experience

# Formulaire Experience

class ExperienceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        self.fields['experience_auteur'].widget.attrs['readonly'] = True
    class Meta:
        model = Experience
        fields = (
                  'experience_auteur',
                  'experience_nom_article',
                  'experience_descriptif',
                  'experience_pub_date',
                  'experience_remedes',
                  'experience_rapport_anomalie',
                  'experience_ift',
                  'experience_photos_1',
                  'experience_photos_2',
                  'experience_document'
                  )
        defaut = forms.ModelMultipleChoiceField(queryset=Defaut.objects.all(),widget=forms.CheckboxSelectMultiple)
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
            'experience_document': forms.HiddenInput(),
            'experience_document': forms.FileInput(),
        }