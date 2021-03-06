# Generated by Django 3.2.7 on 2021-09-23 14:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Webfautheque', '0002_alter_defaut_defaut_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='experience_actions',
            field=models.TextField(default='None', max_length=2000),
        ),
        migrations.AddField(
            model_name='experience',
            name='experience_numero_article',
            field=models.CharField(default='None', max_length=20),
        ),
        migrations.AddField(
            model_name='experience',
            name='experience_photos',
            field=models.FileField(default='None',
                                   upload_to='<django.db.models.fields.related.ForeignKey>/Exp_<django.db.models.fields.DateTimeField>/Photos'),
        ),
        migrations.AddField(
            model_name='experience',
            name='experience_rapport_anomalie',
            field=models.FileField(default='None',
                                   upload_to='<django.db.models.fields.related.ForeignKey>/Exp_<django.db.models.fields.DateTimeField>/Rapport_anomalie'),
        ),
        migrations.AddField(
            model_name='experience',
            name='experience_resultats',
            field=models.TextField(default='None', max_length=2000),
        ),
        migrations.AlterField(
            model_name='defaut',
            name='defaut_image',
            field=models.ImageField(blank=True, default='None',
                                    upload_to='static/Webfautheque/<django.db.models.fields.CharField>/Schema'),
        ),
    ]
