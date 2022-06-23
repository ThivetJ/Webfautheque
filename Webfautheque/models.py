import os

from django.db import models
from django.dispatch import receiver
from django.utils import timezone


class Classe(models.Model):
    """
    Cette classe regroupe le plus haut niveau d' arborescence de la défauthèque
    à savoir les 7 Classes de bases : A, B, C, D, E, F, G
    """
    classe_idperso = models.CharField('Classe', max_length=1)
    classe_nom = models.CharField('Intitulé', max_length=2000)

    def __str__(self):
        return self.classe_idperso


class Groupe(models.Model):
    """Cette classe regroupe le niveau d' arborescence juste en dessous de la classe Classe,
    il corresponds aux groupes de défauts : A100, A200, C100 etc...
    Elle est liée à la classe Classe
    """

    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    groupe_idperso = models.CharField('Nom du groupe', max_length=4)
    groupe_nom = models.CharField('Description ', max_length=2000)

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

    groupe = models.ForeignKey('Groupe', on_delete=models.CASCADE)
    sous_groupe_idperso = models.CharField('Sous groupe', max_length=4)
    sous_groupe_nom = models.CharField('Description', max_length=2000)

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
    defaut_nom = models.CharField('Nom defaut', max_length=2000)
    defaut_image = models.ImageField('Image', upload_to='static/Webfautheque/presentation_defauts',
                                     default="None", blank=True)
    defaut_description = models.TextField('Description', max_length=20000)
    defaut_info = models.TextField('Information', max_length=20000)
    defaut_causes = models.TextField('Causes', max_length=20000)
    defaut_remedes = models.TextField('Remedes', max_length=20000)

    def __str__(self):
        return self.defaut_idperso

    # affiche l'intitulé du sous groupe
    def _sous_groupe(self):
        return self.sous_groupe.sous_groupe_idperso


@receiver(models.signals.post_delete, sender=Defaut)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    '''
    Supprime les images de l'experience
    '''
    if instance.defaut_image:
        if os.path.isfile(instance.defaut_image.path):
            os.remove(instance.defaut_image.path)


@receiver(models.signals.pre_save, sender=Defaut)
def auto_delete_file_on_change(sender, instance, **kwargs):
    '''
    Supprime les images de l'experience
    '''
    if not instance.pk:
        return False
    try:
        old_file = Defaut.objects.get(pk=instance.pk).defaut_image
    except Defaut.DoesNotExist:
        return False
    new_file = instance.defaut_image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class Experience(models.Model):
    """
    Cette classe est lié à un défaut (class Defaut), elle représente une experience de l' utilisateur.
    """
    experience_nom_article = models.CharField(
        'Code expérience', max_length=2000)
    defaut = models.ForeignKey(Defaut,
                               on_delete=models.CASCADE)
    experience_auteur = models.CharField(
        'Auteur', max_length=2000, blank=True,  null=True)
    experience_pub_date = models.DateTimeField('date', default=timezone.now)
    experience_rapport_anomalie = models.CharField(
        'Rapport anomalie', max_length=2000, default="None", blank=True)

    experience_ift = models.CharField(
        'Ift', max_length=2000, default="None", blank=True)
    experience_photos_1 = models.ImageField(
        'Photo 1', upload_to='static/Webfautheque/photos', default="None")
    experience_photos_2 = models.ImageField(
        'Photo 2', upload_to='static/Webfautheque/photos', default="None")
    experience_descriptif = models.TextField(
        'descriptif', max_length=50000, default=" ")
    experience_remedes = models.TextField(
        'remedes', max_length=20000, default="")

    # def __str__(self):
    #     return str(self.defaut) + ' ' + self.experience_auteur + ' ' + str(self.experience_pub_date)

    # affichage intitulé du défaut
    def nom_defaut(self):
        return self.defaut.defaut_nom

    # cas URL sur le reseau / changer le model en CharField / supprimer la condition du rapport dans auto_delete
    def save(self, *args, **kwargs):
        super(Experience, self).save(*args, **kwargs)
        if self.experience_rapport_anomalie:
            path = self.experience_rapport_anomalie
            self.experience_rapport_anomalie = path
        if self.experience_ift:
            path = self.experience_ift
            self.experience_ift = path
        return super(Experience, self).save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=Experience)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    '''
    Supprime les images/fichiers de l'experience
    '''
    if instance.experience_photos_1:
        if os.path.isfile(instance.experience_photos_1.path):
            os.remove(instance.experience_photos_1.path)
    if instance.experience_photos_2:
        if os.path.isfile(instance.experience_photos_2.path):
            os.remove(instance.experience_photos_2.path)


@receiver(models.signals.pre_save, sender=Experience)
def auto_delete_file_on_change(sender, instance, **kwargs):
    '''
    Remplace les images/fichiers si suppression
    '''
    if not instance.pk:
        return False
    try:
        old_file= Experience.objects.get(pk=instance.pk).experience_ift
    except Experience.DoesNotExist:
        return False

    if not old_file == instance.experience_photos_1:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
    if not old_file == instance.experience_photos_2:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)