# Generated by Django 3.2.7 on 2021-09-21 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classe_idperso', models.CharField(max_length=1)),
                ('classe_nom', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Defaut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('defaut_idperso', models.CharField(max_length=4)),
                ('defaut_nom', models.CharField(max_length=200)),
                ('defaut_image', models.ImageField(default='None', upload_to='static/Webfautheque/presentation_defauts')),
                ('defaut_description', models.TextField(max_length=2000)),
                ('defaut_info', models.TextField(max_length=2000)),
                ('defaut_causes', models.TextField(max_length=2000)),
                ('defaut_remedes', models.TextField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupe_idperso', models.CharField(max_length=4)),
                ('groupes_nom', models.CharField(max_length=200)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Webfautheque.classe')),
            ],
        ),
        migrations.CreateModel(
            name='Sous_groupe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sous_groupe_idperso', models.CharField(max_length=4)),
                ('sous_groupe_nom', models.CharField(max_length=200)),
                ('groupe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Webfautheque.groupe')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience_auteur', models.CharField(max_length=200)),
                ('experience_pub_date', models.DateTimeField(verbose_name='date published')),
                ('defaut', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Webfautheque.defaut')),
            ],
        ),
        migrations.AddField(
            model_name='defaut',
            name='sous_groupe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Webfautheque.sous_groupe'),
        ),
    ]
