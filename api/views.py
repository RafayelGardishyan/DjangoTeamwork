from django.shortcuts import render

# Create your views here.
from People.models import People
from Tasks.models import Task, CompletedTask
from Shortener.models import Short
from Plans.models import Plan
from Logs.models import Log
from Ideas.models import Idea
from Files.models import File
from rest_framework import viewsets
from .serializers import UserSerializer, TaskSerializer, CompletedTaskSerializer, PlanSerializer
from .serializers import ShortenerSerializer, IdeaSerializer, LogSerializer, FilesSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = People.objects.all().order_by('-name')
    serializer_class = UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Task.objects.all().order_by('date')
    serializer_class = TaskSerializer


class CompletedTaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = CompletedTask.objects.all().order_by('date')
    serializer_class = CompletedTaskSerializer


class ShortenerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Short.objects.all().order_by('date')
    serializer_class = ShortenerSerializer


class PlanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Plan.objects.all().order_by('deadline')
    serializer_class = PlanSerializer


class LogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Log.objects.all().order_by('added')
    serializer_class = LogSerializer


class IdeaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Idea.objects.all().order_by('name')
    serializer_class = IdeaSerializer


class FileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = File.objects.all().order_by('added_on')
    serializer_class = FilesSerializer
