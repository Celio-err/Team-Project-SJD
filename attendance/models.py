from django.db import models
from users.models import Estudante
from academic.models import Disiplina

class Prezensa(models.Model):
    STATUS_CHOICES = [
        ('Presente', 'Presente'),
        ('Falta', 'Falta'),
        ('Lisensa', 'Lisensa'),
        ('Moras', 'Moras'),
    ]
    # Menghubungkan ke AlokasiMateria di app academic
    alokasi = models.ForeignKey('academic.AlokasiMateria', on_delete=models.CASCADE)
    estudante = models.ForeignKey('users.Estudante', on_delete=models.CASCADE, related_name='prezensas')
    data = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = "Prezensa"
        verbose_name_plural = "Prezensa Sira"

    def __str__(self):
        return f"{self.estudante.naran_kompletu} - {self.data}"
    

# attendance/models.py
class ValorFinalista(models.Model):
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    disiplina = models.ForeignKey(Disiplina, on_delete=models.CASCADE)
    valor = models.IntegerField() # Ini adalah nilai angkanya

    def __str__(self):
        return f"{self.estudante.naran_kompletu} - {self.disiplina.naran_disiplina}"
    
class DokumentuSetting(models.Model):
    data_ezame = models.CharField(max_length=255) # Tempat menyimpan "14 a 18 de Outubro de 2024"
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.data_ezame