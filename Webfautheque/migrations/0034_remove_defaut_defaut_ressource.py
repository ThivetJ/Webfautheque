# Generated by Django 4.0.5 on 2022-07-06 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Webfautheque', '0033_defaut_defaut_ressource'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='defaut',
            name='defaut_ressource',
        ),
    ]