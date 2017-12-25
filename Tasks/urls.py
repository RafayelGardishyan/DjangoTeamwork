from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add', views.add),
    path('complete/<slug:slug>', views.delete, name='task'),
    path('completed/delete/<slug:slug>', views.deleteCompleted, name='task-delete'),
    path('completed', views.indexCompleted),
    path('filter/user', views.filteruser),
    path('filter/date', views.filterdate),
]
