from django.contrib import admin
from .models import Prezensa


@admin.register(Prezensa)
class PrezensaAdmin(admin.ModelAdmin):
    # Gunakan field yang PASTI ada di model Prezensa Anda
    list_display = ('estudante', 'alokasi', 'data', 'status')
    # Kosongkan search_fields dan list_filter dulu untuk tes
    search_fields = []
    list_filter = []