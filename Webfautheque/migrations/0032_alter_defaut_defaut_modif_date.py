# Generated by Django 4.0.5 on 2022-06-30 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Webfautheque', '0031_defaut_defaut_modif_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaut',
            name='defaut_modif_date',
            field=models.DateTimeField(blank=True, default=None, verbose_name='Date de modification'),
        ),
    ]
