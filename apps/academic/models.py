from django.db import models

from apps.users.models import Professor

class Klase(models.Model):
    DEPARTAMENTU_CHOICES = [('CN', 'Ciencias Naturais'), ('CSH', 'Ciencias Sociais e Humanidades')]
    NIVEL_CHOICES = [('10', '10'), ('11', '11'), ('12', '12')]
    nivel = models.CharField(max_length=2, choices=NIVEL_CHOICES)
    departamentu = models.CharField(max_length=3, choices=DEPARTAMENTU_CHOICES)
    turma = models.CharField(max_length=5) # Contoh: A, B, atau C

    def __str__(self):
        return f"{self.nivel} {self.departamentu} {self.turma}"

class Disiplina(models.Model):
    DEPARTAMENTU_CHOICES = [('CN', 'IPA (CN)'), ('CSH', 'IPS (CSH)'), ('Geral', 'Geral')]
    naran_disiplina = models.CharField(max_length=100, unique=True)
    kodigu = models.CharField(max_length=10, unique=True)
    departamentu = models.CharField(max_length=10, choices=DEPARTAMENTU_CHOICES) # Kunci Otomatisasi

    def __str__(self):
        return self.naran_disiplina

class AlokasiMateria(models.Model):
    disiplina = models.ForeignKey(Disiplina, on_delete=models.CASCADE)
    # Tambahkan null=True dan blank=True di bawah ini
    klase = models.ForeignKey(Klase, on_delete=models.SET_NULL, null=True, blank=True)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('disiplina', 'klase')

    def __str__(self):
        return f"{self.disiplina} - {self.klase}"
    
class MisaunVizaun(models.Model):
    titulu =  models.CharField(max_length=100, blank=False, null=False)
    deskrisaun = models.TextField()

    def __str__(self):
            return self.titulu
        
