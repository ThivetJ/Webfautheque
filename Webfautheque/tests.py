# Create your tests here.
import datetime
import random
from django.shortcuts import redirect

from requests import request
from faker import Faker

from Webfautheque.models import Experience
from Webfautheque.models import *

#url, n'envoie pas des fichiers sur le serveur
list = ['5829-9-001_Crasse_brides_usinage_(13).jpg', '4772-1_(1).jpg', '20190910_082839.jpg', 'fausse_serre_6051-8-004.jpg', 'oubli_enduit.jpg', 'carter_4480-2.jpg']
fake = Faker()


for i in range(120):
    experience = Experience(experience_nom_article=fake.sentence(),
                            experience_descriptif=fake.paragraph(nb_sentences=random.randint(5, 15)),
                            experience_remedes=fake.paragraph(nb_sentences=random.randint(5, 15)),
                            experience_pub_date=datetime.datetime.now(),
                            experience_auteur= 'admin',
                            defaut_id= random.randint(1, 100),
                            experience_ift = 'static/Webfautheque/ift/'+list[random.randint(0, 5)],
                            experience_photos_1 = 'static/Webfautheque/photos/'+list[random.randint(0, 5)], 
                            experience_photos_2 = 'static/Webfautheque/photos/'+list[random.randint(0, 5)], 
                            experience_rapport_anomalie = 'static/Webfautheque/rapport_anomalie/'+list[random.randint(0, 5)],
    )
    experience.save()
