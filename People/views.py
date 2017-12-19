from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from .models import People
# Create your views here.
def index(request):
    people = People.objects.order_by('name')
    template = loader.get_template('people/index.html')
    context = {
        'people': people,
    }
    return HttpResponse(template.render(context, request))

def add(request):
    if 'n' in request.GET:
        one = People()
        one.name = request.GET['n']
        one.birthDate = request.GET['bd']
        one.rang = request.GET['r']
        one.save()
        return HttpResponse("<a href=\"/people\"> Homepage </a>")
    else:
        context = {'message': "Add new users"}
        template = loader.get_template('people/add.html')
        return HttpResponse(template.render(context, request))

