# Generated by Django 4.0.3 on 2022-05-10 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Webfautheque', '0023_remove_experience_experience_ift_2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='experience_nom_article',
            field=models.CharField(max_length=200, verbose_name='Code expérience'),
        ),
    ]
