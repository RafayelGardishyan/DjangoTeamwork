from People.models import People
from Tasks.models import Task, CompletedTask
from Shortener.models import Short
from Plans.models import Plan
from Logs.models import Log
from Ideas.models import Idea
from Files.models import File
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = People
        fields = ('name', 'rang', 'birthDate', 'activated', 'slug')


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('name', 'user', 'date', 'slug', 'inprogress')


class CompletedTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CompletedTask
        fields = ('name', 'user', 'date', 'slug', 'completed_on')


class ShortenerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Short
        fields = ('slug', 'link')


class PlanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plan
        fields = ('name', 'description', 'deadline', 'slug')


class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ('title', 'text', 'user', 'added', 'slug')


class IdeaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Idea
        fields = ('name', 'description', 'slug')


class FilesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ('name', 'file', 'added_on', 'slug')
