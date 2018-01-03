"""DjangoTeam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from Start import views as sv

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', sv.index),
    path('logout/', sv.delete),
    path('activate/<slug:slug>/<str:rang>/<str:sk>/<str:ac>', sv.activate, name='activate'),
    path('activate', sv.siteact),
    path('tasks/', include('Tasks.urls')),
    path('people/', include('People.urls')),
    path('ideas/', include('Ideas.urls')),
    path('plans/', include('Plans.urls')),
    path('files/', include('Files.urls')),
    path('logs/', include('Logs.urls')),
    path('calendar/', include('Calendar.urls')),
    path('s/', include('Shortener.urls')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
