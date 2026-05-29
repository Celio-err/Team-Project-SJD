from django.contrib import admin

from apps.users.models import Estudante, Professor

# Register your models here.
@admin.register(Estudante)
class EstudanteAdmin(admin.ModelAdmin):
    list_display = ('nu_emis', 'naran_kompletu', 'sexu', 'klase', 'status')
    search_fields = ('naran_kompletu', 'nu_emis')

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nis', 'id_funcionario', 'naran_kompletu', 'status', 'nu_telemovel', 'cargo')