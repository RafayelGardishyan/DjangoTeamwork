from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add', views.add),
    path('delete/<slug:slug>', views.delete, name='delete-plans'),
    path('description/<slug:slug>', views.description, name='description-plans'),
]
