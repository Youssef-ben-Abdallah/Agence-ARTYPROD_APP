from datetime import date, timezone
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db import models


class Personnell(models.Model):
    nom = models.CharField(max_length=255)
    cv = models.FileField(upload_to='cvs/')
    photo = models.ImageField(upload_to='photos/')
    lien_LinkedIn = models.URLField(blank=True)
    def __str__(self):
        return self.nom 

class Projett(models.Model):
    libell = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    date_debut = models.DateField(null=True, default=date.today)
    date_fin = models.DateField(null=True, blank=True)
    achevé = models.CharField(max_length=1, default='N', choices=[('N','non'),('O','oui')])
    equipe = models.ForeignKey('Equipe', on_delete=models.CASCADE)
    user_id = models.IntegerField(default=0)  
    created_by_admin = models.BooleanField(default=False)
    def __str__(self):
        return self.libell 
    
class Service(models.Model):
    nom = models.CharField(max_length=100)
    type =models.CharField(max_length=20,default='Charte graphique',choices=[('Charte graphique','Charte graphique'),('Objet 3D','Objet 3D'),('Scénarisation','Scénarisation')])
    description = models.TextField()
    
    def __str__(self):
        return self.nom

class Detail(models.Model):
    projet = models.ForeignKey(Projett, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.projet.titre + ' - ' + self.service.nom



class Equipe(models.Model):
    personne = models.ManyToManyField('Personnell')
    def __str__(self):
        membres_str = ", ".join(self.personne.values_list('nom', flat=True))
        return f"({membres_str})"
   
    
class Contact(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    tel = models.CharField(max_length=20)
    service=models.ForeignKey('Service', on_delete=models.CASCADE)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.date_envoi}"
    



class Commentaire(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.user.username}"
