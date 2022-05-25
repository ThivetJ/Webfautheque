import os
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from requests import delete
from pathlib import Path, PureWindowsPath

class Classe(models.Model):
    """
    Cette classe regroupe le plus haut niveau d' arborescence de la défauthèque
    à savoir les 7 Classes de bases : A, B, C, D, E, F, G
    """
    classe_idperso = models.CharField('Classe', max_length=1)
    classe_nom = models.CharField('Intitulé', max_length=200)

    def __str__(self):
        return self.classe_idperso


class Groupe(models.Model):
    """Cette classe regroupe le niveau d' arborescence juste en dessous de la classe Classe,
    il corresponds aux groupes de défauts : A100, A200, C100 etc...
    Elle est liée à la classe Classe
    """

    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    groupe_idperso = models.CharField('Nom du groupe', max_length=4)
    groupe_nom = models.CharField('Description ', max_length=200)

    def __str__(self):
        return self.groupe_idperso

    # affiche l'intitulé de la classe
    def nom_classe(self):
        return self.classe.classe_idperso 
            
class Sous_groupe(models.Model):
    """Cette classe regroupe le niveau d' arborescence juste en dessous des Groupe,
    il correspond aux sous-groupes de défaut :  A110, A120, C130 etc ...
    Elle est liée à la classe Groupe
    """

    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    sous_groupe_idperso = models.CharField('Sous groupe', max_length=4)
    sous_groupe_nom = models.CharField('Sous groupe', max_length=200)
    
    def __str__(self):
        return self.sous_groupe_idperso

    # affiche l'intitulé du groupe
    def nom_groupe(self):
        return self.groupe.groupe_idperso


class Defaut(models.Model):
    """
    Cette classe regroupe le dernier niveau d' arborescence de la défauthèque,
    il s' agit des défauts : A111, A123, C131 etc...
    Elle référence toutes les informations générales à savoir sur un défaut (nom, description, info, causes, remèdes)
    Elle est liée à la classe sous_groupe
    """
    sous_groupe = models.ForeignKey(Sous_groupe, on_delete=models.CASCADE)
    defaut_idperso = models.CharField('Code defaut', max_length=4)
    defaut_nom = models.CharField('Nom defaut', max_length=200)
    defaut_image = models.ImageField('Image', upload_to='static/Webfautheque/presentation_defauts',
                                     default="None", blank=True)
    # une petite phrase de description simple
    defaut_description = models.TextField('Description', max_length=2000)
    defaut_info = models.TextField('Information', max_length=2000)
    defaut_causes = models.TextField('Causes', max_length=2000)
    defaut_remedes = models.TextField('Remedes', max_length=2000)

    def __str__(self):
        return self.defaut_idperso

    # affiche l'intitulé du sous groupe
    def _sous_groupe(self):
        return self.sous_groupe.sous_groupe_idperso

class Experience(models.Model):
    """
    Cette classe est lié à un défaut (class Defaut), elle représente une experience de l' utilisateur.

    """
    experience_nom_article = models.CharField(
        'Code expérience', max_length=200)
    defaut = models.ForeignKey(Defaut,
                               on_delete=models.CASCADE)
    experience_auteur = models.CharField(
        'Auteur', max_length=200, blank=True,  null=True)
    experience_pub_date = models.DateTimeField('date', default=timezone.now)
    experience_rapport_anomalie = models.FileField(
        'rapport anomalie ', upload_to='static/Webfautheque/rapport_anomalie', default="None")
    experience_ift = models.ImageField(
        'Ift', upload_to='static/Webfautheque/ift', default="None")
    experience_photos_1 = models.ImageField(
        'Photo_1', upload_to='static/Webfautheque/photos', default="None")
    experience_photos_2 = models.ImageField(
        'Photo_2', upload_to='static/Webfautheque/photos', default="None")
    experience_descriptif = models.TextField(
        'descriptif', max_length=5000, default=" ")
    experience_remedes = models.TextField(
        'remedes', max_length=2000, default="")
    
    
    # def __str__(self):
    #     return str(self.defaut) + ' ' + self.experience_auteur + ' ' + str(self.experience_pub_date)

    # affichage intitulé du défaut
    def nom_defaut(self):
        return self.defaut.defaut_idperso+': '+self.defaut.defaut_nom

@receiver(models.signals.post_delete, sender=Experience)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    '''
    Supprime les images de l'experience
    '''
    if instance.experience_ift:
        if os.path.isfile(instance.experience_ift.path):
            os.remove(instance.experience_ift.path)
    if instance.experience_rapport_anomalie:
        if os.path.isfile(instance.experience_rapport_anomalie.path):
            os.remove(instance.experience_rapport_anomalie.path)
    if instance.experience_photos_1:
        if os.path.isfile(instance.experience_photos_1.path):
            os.remove(instance.experience_photos_1.path)
    if instance.experience_photos_2:
        if os.path.isfile(instance.experience_photos_2.path):
            os.remove(instance.experience_photos_2.path)


@receiver(models.signals.pre_save, sender=Experience)
def auto_delete_file_on_change(sender, instance, **kwargs):
    '''
    Remplace les images si elle est modifiée
    '''
    if not instance.pk:
        return False
    try:
        old_file= Experience.objects.get(pk=instance.pk).experience_ift
    except Experience.DoesNotExist:
        return False


    if not old_file == instance.experience_ift:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
    if not old_file == instance.experience_rapport_anomalie:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
    if not old_file == instance.experience_photos_1:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
    if not old_file == instance.experience_photos_2:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
