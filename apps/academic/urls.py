from django.urls import path
from . import views  
urlpatterns = [
    path('disiplina/foun/', views.disiplina_create_view, name='disiplina_create'),
    path('disiplina/lista/', views.disiplina_list_view, name='disiplina_list'),
    path('disiplina/hamoos/<int:pk>/', views.hamoos_disiplina, name='hamoos_disiplina'),
    path('disiplina/edit/<int:pk>/', views.edit_disiplina, name='edit_disiplina'),
    path('klase/lista/', views.klase_list_view, name='lista_klase'),
    path('klase/foun/', views.klase_create, name='klase_create'),
    path('klase/delete/<int:pk>/', views.hamoos_klase, name='delete_klase'),
    path('klase/edit/<int:pk>/', views.edit_klase, name='edit_klase'),
    path('alokasaun/', views.alokasi_list, name='alokasaun_list'),
    path('alokasaun/foun/', views.alokasaun_create, name='alokasaun_create'),
    path('alokasaun/konfigura/<int:pk>/', views.konfig_alokasaun, name='konfig_alokasaun'),
    path('prezensa/<int:klase_id>/', views.estudante_kada_klase, name='lista_prezensa'),
    path('alokasaun/delete/<int:pk>/', views.hamoos_alokasaun, name='delete_alokasaun'),
    path('academic/misaun-vizaun', views.vizaun_misaun, name='vizaun_misaun'),
]