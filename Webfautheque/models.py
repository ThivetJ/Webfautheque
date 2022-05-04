from django.db import models
from django.utils import timezone


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
    groupe_idperso = models.CharField('Groupe', max_length=4)
    groupe_nom = models.CharField('Intitulé', max_length=200)

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
    sous_groupe_nom = models.CharField('Nom sous groupe', max_length=200)

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
    defaut_idperso = models.CharField('Defaut', max_length=4)
    defaut_nom = models.CharField('Nom', max_length=200)
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
    defaut = models.ForeignKey(Defaut,
                               on_delete=models.CASCADE)
    experience_auteur = models.CharField(
        'Auteur', max_length=200, blank=True,  null=True)
    experience_pub_date = models.DateTimeField('date', default=timezone.now)
    experience_nom_article = models.CharField(
        'nom de l\'article', max_length=200)
    # tentative d' upload to : f'{defaut}/Exp_{experience_pub_date}/Rapport_anomalie'
    experience_rapport_anomalie = models.FileField(
        'rapport anomalie ', upload_to='static/Webfautheque/rapport_anomalie', default="None")
    experience_ift = models.FileField(
        'Ift', upload_to='static/Webfautheque/ift', default="None")
    experience_photos = models.FileField(
        'Photo', upload_to='static/Webfautheque/photos', default="None")
    experience_descriptif = models.TextField(
        'descriptif', max_length=2000, default=" ")
    experience_remedes = models.TextField(
        'remedes', max_length=2000, default="")
    
    def __str__(self):
        return str(self.defaut) + ' ' + self.experience_auteur + ' ' + str(self.experience_pub_date)

    # affichage intitulé du défaut
    def nom_defaut(self):
        return self.defaut.defaut_idperso
