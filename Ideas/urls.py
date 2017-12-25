from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add', views.add),
    path('delete/<slug:slug>', views.delete, name='delete-ideas'),
    path('description/<slug:slug>', views.description, name='description-ideas'),
]
