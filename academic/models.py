from django.db import models

from users.models import Professor

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
    
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# ... (Tetap biarkan model Klase, Disiplina, dan AlokasiMateria Anda yang sudah ada)

# @receiver(post_save, sender=Klase)
# def alokasi_materia_automatiku(sender, instance, created, **kwargs):
#     if created:
#         # 1. Cari pelajaran yang departemennya cocok (CN/CSH) ATAU yang bersifat 'Geral'
#         disiplinas = Disiplina.objects.filter(
#             models.Q(departamentu=instance.departamentu) | models.Q(departamentu='Geral')
#         )
        
#         # 2. Buat AlokasiMateria untuk setiap pelajaran yang ditemukan
#         # Karena guru belum diketahui, kita biarkan null atau pilih guru default
#         for materia in disiplinas:
#             AlokasiMateria.objects.get_or_create(
#                 disiplina=materia,
#                 klase=instance,
#                 # Catatan: Lapangan 'professor' di model Anda harus allow null=True 
#                 # jika ingin benar-benar otomatis tanpa guru di awal.
#                 # Jika tidak, kita bisa abaikan dulu bagian ini atau buat guru 'Temporary'
#             )