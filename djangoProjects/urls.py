"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from Webfautheque import views

urlpatterns = [
    # ex: /index/
    re_path(r'^home/$',
        views.home,
        name="home"),

    # ex: /Webfautheque/admin/
    path('admin/', admin.site.urls),

    # ex: /Presentation/
    re_path(r'^Présentation/$',
        views.page_presentation_defautheque,
        name="page_presentation_defautheque"),

    # ex: /Webfautheque/Arborescence/
    re_path(r'^Webfautheque/Arborescence/$',
        views.page_arborescence_defautheque,
        name="page_arborescence_defautheque"),

    # ex: /Webfautheque/A/
    re_path(r'^Webfautheque/(?P<classe_idperso>[A-G]{1})/$',
        views.page_groupes_defautheque,
        name="page_groupes_defautheque"),

    # ex: /Webfautheque/A100/
    re_path(r'^Webfautheque/(?P<classe_idperso>[A-G]{1})(?P<groupe_idperso_one_char>[1-9]{1})00/$',
        views.page_sous_groupes_defautheque,
        name="page_sous_groupes_defautheque"),

    # ex: /Webfautheque/A110/
    re_path(r'^Webfautheque/(?P<classe_idperso>[A-G]{1})(?P<groupe_idperso_one_char>[1-9]{1})(?P<sous_groupe_idperso_one_char>[1-9]{1})0/$',
        views.page_defauts_defautheque,
        name="page_defauts_defautheque"),

    # ex: /Webfautheque/A111/
    re_path(r'^Webfautheque/(?P<defaut_idperso>[A-G]{1}[1-9]{3})/$',
        views.page_presentation_defaut,
        name="page_presentation_defaut"),

    # ex: /Webfautheque/A111/Experiences/
    re_path(r'^Webfautheque/(?P<defaut_idperso>[A-G]{1}[1-9]{3})/Experiences/$',
        views.page_choix_experience,
        name="page_choix_experience"),

    # ex: /Webfautheque/A111/Experiences/Consultation:1/
    re_path(r'^Webfautheque/(?P<defaut_idperso>[A-G]{1}[1-9]{3})/Experiences/Consultation:(?P<experience_id>[0-9]+)/$',
        views.page_consultation_experience,
        name="page_consultation_experience"),

    # ex: /Webfautheque/A111/Experiences/Ajout/
    re_path(r'^Webfautheque/(?P<defaut_idperso>[A-G]{1}[1-9]{3})/Experiences/Ajout/$',
        views.page_ajout_experience,
        name="page_ajout_experience"),
]