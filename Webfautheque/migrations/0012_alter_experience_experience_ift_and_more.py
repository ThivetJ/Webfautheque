# Generated by Django 4.0.3 on 2022-04-11 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Webfautheque', '0011_alter_experience_experience_ift_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='experience_ift',
            field=models.ImageField(upload_to='static/Webfautheque/ift'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='experience_photos',
            field=models.ImageField(upload_to='static/Webfautheque/photos'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='experience_rapport_anomalie',
            field=models.FileField(upload_to='static/Webfautheque/rapport_anomalie'),
        ),
    ]