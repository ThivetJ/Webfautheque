from django.db import models


class Classe(models.Model):
    """Cette classe regroupe le plus haut niveau d'arborescence de la défauthèque à savoir les 7 Classes de bases : A, B, C, D, E, F, G"""
    classe_idperso = models.CharField(max_length=1)
    classe_nom = models.CharField(max_length=200)

    def __str__(self):
        return self.classe_idperso


class Groupe(models.Model):
    """Cette classe regroupe le niveau d'arborescence juste en dessous de la classe Classe, il corresponds aux groupes de défauts : A100, A200, C100 etc...
    Elle est liée à la classe Classe
    """

    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    groupe_idperso = models.CharField(max_length=4)
    groupes_nom = models.CharField(max_length=200)

    def __str__(self):
        return self.groupe_idperso


class Sous_groupe(models.Model):
    """Cette classe regroupe le niveau d'arborescence juste en dessous des Groupe, il correspond aux sous-groupes de défaut :  A110, A120, C130 etc ...
    Elle est liée à la classe Groupe
    """

    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    sous_groupe_idperso = models.CharField(max_length=4)
    sous_groupe_nom = models.CharField(max_length=200)

    def __str__(self):
        return self.sous_groupe_idperso


class Defaut(models.Model):
    """
    Cette classe regroupe le dernier niveau d'arborescence de la défautheque, il s'agit des défauts : A111, A123, C131 etc...
    Elle référence toutes les informations générales à savoir sur un défaut (nom, description, info, causes, remedes)
    Elle est liée à la classe sous_groupe
    """
    sous_groupe = models.ForeignKey(Sous_groupe, on_delete=models.CASCADE)
    defaut_idperso = models.CharField(max_length=4)
    defaut_nom = models.CharField(max_length=200)
    defaut_image = models.ImageField(upload_to='static/Webfautheque/presentation_defauts', default="None", blank=True)
    defaut_description = models.TextField(max_length=2000)  # une petite phrase de description simple
    defaut_info = models.TextField(max_length=2000)
    defaut_causes = models.TextField(max_length=2000)
    defaut_remedes = models.TextField(max_length=2000)

    def __str__(self):
        return self.defaut_idperso

    def is_class_A(self):
        """Ceci est une méthode test"""
        if self.defaut_idperso[0] == "A":
            return True
        else:
            return False


class Experience(models.Model):
    """
    Cette classe est lié à un défaut (class Defaut), elle représente une experience de l'utilisateur.

    """
    # TODO : enrichir l'objet experience
    defaut = models.ForeignKey(Defaut,
                               on_delete=models.CASCADE)
    experience_auteur = models.CharField(max_length=200)
    experience_pub_date = models.DateTimeField('date published')

    def __str__(self):
        return str(self.defaut) + ' ' + self.experience_auteur + ' ' + str(self.experience_pub_date)
