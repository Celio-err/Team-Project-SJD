from django.urls import path
from .views import dashboard_view, edit_estudante, edit_professor, estudante_create_view, estudante_list_view, hamoos_estudante, hamoos_profesor, professor_create_view, professor_list_view, user_list_view, user_create_view,user_delete_view

urlpatterns = [
    path('estudante/lista/', estudante_list_view, name='estudante_list'), # Halaman list
    path('estudante/foun/', estudante_create_view, name='estudante_create'), # Halaman input
    path('estudante/hamoos/<int:pk>/', hamoos_estudante, name='hamoos_estudante'), # Hapus estudante
    path('estudante/edit/<int:pk>/', estudante_create_view, name='edit_estudante'), # Edit estudante
    path('profesor/lista/', professor_list_view, name='professor_list'), # Halaman list
    path('professor/foun/', professor_create_view, name='professor_create'), # Halaman input
    path('professor/hamoos/<int:pk>/', hamoos_profesor, name='hamoos_professor'), # Hapus professor
    path('professor/edit/<int:pk>/', edit_professor, name='edit_professor'), # Edit professor
    path('management/users/', user_list_view, name='user_list'),
path('management/users/foun/', user_create_view, name='user_create'),
path('management/users/delete/<int:pk>/', user_delete_view, name='user_delete'),
]