# academic/admin.py
from django.apps import AppConfig
from django.contrib import admin
# Hapus Inskrisaun dari sini
from .models import Disiplina, Klase, AlokasiMateria 

@admin.register(Klase)
class KlaseAdmin(admin.ModelAdmin):
    list_display = ('nivel', 'departamentu', 'turma')

@admin.register(AlokasiMateria)
class AlokasiMateriaAdmin(admin.ModelAdmin):
    list_display = ('disiplina', 'klase', 'professor')

admin.site.register(Disiplina)
# admin.site.register(Inskrisaun) <-- Beri komentar atau hapus ini

class AcademicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'academic'

    def ready(self):
        # Tambahkan baris ini untuk mengimpor signals saat aplikasi siap
        import academic.signals