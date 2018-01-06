from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'completed-tasks', views.CompletedTaskViewSet)
router.register(r'plans', views.PlanViewSet)
router.register(r'logs', views.LogViewSet)
router.register(r'ideas', views.IdeaViewSet)
router.register(r'files', views.FileViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]