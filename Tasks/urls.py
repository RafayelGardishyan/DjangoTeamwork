from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add', views.add),
    path('<slug:slug>', views.delete, name='task')
]
