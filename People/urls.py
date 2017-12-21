from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add', views.add),
    path('delete/<slug:slug>', views.delete, name='people'),
]
