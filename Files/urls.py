from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('delete/<slug:slug>', views.delete, name='delete-files'),
    path('add', views.add)
]
