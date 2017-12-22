from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add', views.add, name='delete-plans'),
    path('delete/<slug:slug>', views.delete, name='delete-plans'),
]
