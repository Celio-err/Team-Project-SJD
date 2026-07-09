from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Professor(models.Model):
    STATUS_CHOICES = [
        ('Permanente', 'Permanente'), 
        ('Kontratadu', 'Kontratadu'), 
        ('Voluntariu', 'Voluntariu')
    ]
    CARGO_CHOICE = [
        ('Professor', 'Professor'), 
        ('Diretor/a da Escola', 'Diretor/a da Escola')
    ]
    # Menghubungkan ke Auth User (Bertindak sebagai Perfil)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='professor_profile')    
    nis = models.CharField(max_length=20, unique=True, null=True, blank=True)
    id_funcionario = models.CharField(max_length=20, unique=True, null=True, blank=True)
    # Field yang akan sinkron dengan profil pengguna
    naran_kompletu = models.CharField(max_length=255)
    nu_telemovel = models.CharField(max_length=15, unique=True)
    
    # Field yang biasanya hanya ditentukan oleh Admin
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Permanente')
    cargo = models.CharField(max_length=25, choices=CARGO_CHOICE, null=True, default='Professor')
    
    def __str__(self):
        return self.naran_kompletu


class Estudante(models.Model):
    SEXU_CHOICES = [('Mane', 'Mane'), ('Feto', 'Feto')]
    nu_emis = models.CharField(max_length=20, unique=True)
    naran_kompletu = models.CharField(max_length=255)
    sexu = models.CharField(max_length=10, choices=SEXU_CHOICES)
    foto = models.ImageField(upload_to='estudante_fotos/', null=True, blank=True)
    klase = models.ForeignKey('academic.Klase', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default="Ativu")

    def __str__(self):
        return f"{self.nu_emis} - {self.naran_kompletu}"