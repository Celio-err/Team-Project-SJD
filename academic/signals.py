from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Disiplina, AlokasiMateria

# @receiver(post_save, sender=Disiplina)
# def kria_draft_alokasaun(sender, instance, created, **kwargs):
#     if created:
#         # Membuat hanya satu baris alokasi "Draft" tanpa Kelas & Profesor
#         AlokasiMateria.objects.create(
#             disiplina=instance,
#             klase=None,       # Akan muncul sebagai (-) di tabel
#             professor=None,   # Akan muncul sebagai (-) di tabel
#         )