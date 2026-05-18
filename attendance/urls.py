from django.urls import path
from . import views  # Mengambil views dari folder attendance itu sendiri

urlpatterns = [
path('finalista/klase/', views.lista_klase_finalista, name='lista_klase_finalista'),
path('finalista/klase/<int:klase_id>/estudantes/', views.lista_estudante_finalista, name='lista_estudante_finalista'),
path('finalista/input-valor/<int:estudante_id>/', views.input_valor_estudante, name='input_valor_estudante'),
path('finalista/print-deklarasaun/<int:estudante_id>/', views.print_deklarasaun, name='print_deklarasaun'),
]