# Generated by Django 4.0.5 on 2022-07-06 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Webfautheque', '0035_experience_experience_document_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experience',
            name='experience_modif_date',
        ),
    ]