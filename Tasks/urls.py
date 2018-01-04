from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add', views.add),
    path('complete/<slug:slug>', views.delete, name='task'),
    path('progress/<slug:slug>', views.progress, name='progress'),
    path('completed/delete/<slug:slug>', views.deleteCompleted, name='task-delete'),
    path('completed', views.indexCompleted),
    path('stats', views.stats),
    path('filter/user', views.filteruser),
    path('filter/date', views.filterdate),
]
