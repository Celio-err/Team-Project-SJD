"""
URL configuration for SJD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from SJD import settings
from academic import views
from django.conf.urls.static import static
from users import views
from users.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard', dashboard_view, name='dashboard'), # Halaman utama
    path('users/', include('users.urls')), # URL untuk aplikasi users
    path('academic/', include('academic.urls')), # URL untuk aplikasi academic
    path('attendance/', include('attendance.urls')), # URL untuk aplikasi attendance
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
