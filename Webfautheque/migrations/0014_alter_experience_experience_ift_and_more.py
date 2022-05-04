# Generated by Django 4.0.3 on 2022-04-11 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Webfautheque', '0013_alter_experience_experience_ift_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='experience_ift',
            field=models.FileField(default='None', upload_to='static/Webfautheque/ift'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='experience_photos',
            field=models.FileField(default='None', upload_to='static/Webfautheque/photos'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='experience_rapport_anomalie',
            field=models.FileField(default='None', upload_to='static/Webfautheque/rapport_anomalie'),
        ),
    ]