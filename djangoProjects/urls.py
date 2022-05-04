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
from Webfautheque import views
from django.contrib import admin
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    # racine 
    re_path(r'^$',
            views.home,
            name=""),

    # ex: /index/
    re_path(r'^home/$',
            views.home,
            name="home"),

    # ex: /Webfautheque/admin/
    path('admin/', admin.site.urls),

    # ex: /Webfautheque/Arborescence/
    re_path(r'^Webfautheque/Arborescence/$',
            views.page_arborescence_defautheque,
            name="page_arborescence_defautheque"),

    # ex: /Webfautheque/A/
    re_path(r'^Webfautheque/(?P<classe_idperso>[A-G])/$',
            views.page_groupes_defautheque,
            name="page_groupes_defautheque"),

    # ex: /Webfautheque/A100/
    re_path(r'^Webfautheque/(?P<classe_idperso>[A-G])(?P<groupe_idperso_one_char>[1-9])00/$',
            views.page_sous_groupes_defautheque,
            name="page_sous_groupes_defautheque"),

    # ex: /Webfautheque/A110/
    re_path(
        r'^Webfautheque/(?P<classe_idperso>[A-G])(?P<groupe_idperso_one_char>[1-9])(?P<sous_groupe_idperso_one_char>[1-9])0/$',
        views.page_defauts_defautheque,
        name="page_defauts_defautheque"),

    # ex: /Webfautheque/A111/
    re_path(r'^Webfautheque/(?P<defaut_idperso>[A-G][1-9]{3})/$',
            views.page_presentation_defaut,
            name="page_presentation_defaut"),

    # ex: /Webfautheque/A111/Experiences/
    re_path(r'^Webfautheque/(?P<defaut_idperso>[A-G][1-9]{3})/Experiences/$',
            views.page_choix_experience,
            name="page_choix_experience"),

    # ex: /Webfautheque/A111/Experiences/Consultation:1/
    re_path(r'^Webfautheque/(?P<defaut_idperso>[A-G][1-9]{3})/Experiences/Consultation:(?P<experience_id>[0-9]+)/$',
            views.page_consultation_experience,
            name="page_consultation_experience"),

    # ex: /Webfautheque/A111/Experiences/Ajout/
    re_path(r'^Webfautheque/(?P<defaut_idperso>[A-G][1-9]{3})/Experiences/Ajout/$',
            views.page_ajout_experience,
            name="page_ajout_experience"),

    # ex: /Webfautheque/Experiences/Ajout/
    re_path(r'^Webfautheque/Experiences/Ajout/$',
            views.page_ajout_experience,
            name="page_ajout_experience_defaut"),

        # ex: /Webfautheque/A111/Experiences/Update/
    re_path(r'^Webfautheque/(?P<id>[A-G][1-9]{3})/Experiences/Consultation:(?P<experience_id>[0-9]+)/Update/$',
            views.page_update_experience,
            name="page_update_experience"),

        # ex: /Webfautheque/A111/Experiences/Delete/
        re_path(r'^Webfautheque/(?P<id>[A-G][1-9]{3})/Experiences/Consultation:(?P<experience_id>[0-9]+)/Delete/$',
                views.page_delete_experience,
                name="page_delete_experience"),

    # ex: /Webfautheque/experiences/
        re_path(r'^Webfautheque/experiences', 
                views.experience_list,
                name="experience_list"),
    # ex: /Webfautheque/login/
        re_path(r'login/', 
                views.login_user,
                name="login_user"),
    # ex: /Webfautheque/logout/
        re_path(r'logout/', 
                views.logout_user,
                name="logout_user"),
    # ex: /Webfautheque/experiences/search-experiences/
        re_path(r'experiences/search_experiences', 
                csrf_exempt(views.search_experiences),
                name="search_experiences"),

        re_path(r'experiences/(?P<defaut_idperso>[A-G][1-9]{3})/search_experiences_by_defaut', 
                csrf_exempt(views.search_experiences_by_defaut),
                name="search_experiences_by_defaut"),
                
        #ajout d'un jeu de donnnées
        #fakerExperience
        # re_path(r'experiences/faker_experiences',
        #         views.fakerExperience,
        #         name="faker_experiences"),

]
