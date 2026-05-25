from django.urls import path
from .views import dashboard_view, edit_estudante, edit_professor, estudante_create_view, estudante_list_view, hamoos_estudante, hamoos_profesor, professor_create_view, professor_list_view

urlpatterns = [
    path('estudante/lista/', estudante_list_view, name='estudante_list'), # Halaman list
    path('estudante/foun/', estudante_create_view, name='estudante_create'), # Halaman input
    path('estudante/hamoos/<int:pk>/', hamoos_estudante, name='hamoos_estudante'), # Hapus estudante
    path('estudante/edit/<int:pk>/', estudante_create_view, name='edit_estudante'), # Edit estudante
    path('profesor/lista/', professor_list_view, name='professor_list'), # Halaman list
    path('professor/foun/', professor_create_view, name='professor_create'), # Halaman input
    path('professor/hamoos/<int:pk>/', hamoos_profesor, name='hamoos_professor'), # Hapus professor
    path('professor/edit/<int:pk>/', edit_professor, name='edit_professor'), # Edit professor
]