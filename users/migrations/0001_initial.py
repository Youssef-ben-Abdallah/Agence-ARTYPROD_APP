# Generated by Django 4.1.2 on 2023-05-21 19:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Personnell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('cv', models.FileField(upload_to='cvs/')),
                ('photo', models.ImageField(upload_to='photos/')),
                ('lien_LinkedIn', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('Charte graphique', 'Charte graphique'), ('Objet 3D', 'Objet 3D'), ('Scénarisation', 'Scénarisation')], default='Charte graphique', max_length=20)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Projett',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libell', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1000)),
                ('date_debut', models.DateField(default=datetime.date.today, null=True)),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('achevé', models.CharField(choices=[('N', 'non'), ('O', 'oui')], default='N', max_length=1)),
                ('equipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.equipe')),
            ],
        ),
        migrations.AddField(
            model_name='equipe',
            name='personne',
            field=models.ManyToManyField(to='users.personnell'),
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fichier', models.FileField(upload_to='uploads/')),
                ('projet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.projett')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.service')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('tel', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('date_envoi', models.DateTimeField(auto_now_add=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.service')),
            ],
        ),
    ]