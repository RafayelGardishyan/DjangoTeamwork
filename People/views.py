from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from .models import People
# Create your views here.
def index(request):
    if request.session.get('logged_in'):
        people = People.objects.order_by('name')
        template = loader.get_template('people/index.html')
        context = {
            'people': people,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def add(request):
    if request.session.get('logged_in'):
        if 'n' in request.GET:
            one = People()
            one.name = request.GET['n']
            one.birthDate = request.GET['bd']
            one.rang = request.GET['r']
            one.secretKey = request.GET['sk']
            one.saveslug(request.GET['n'])
            one.save()
            return HttpResponse("<a href=\"/people\"> Homepage </a>")
        else:
            context = {'message': "Add new users"}
            template = loader.get_template('people/add.html')
            return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def delete(request, slug):
    if request.session.get('logged_in'):
        user = People.objects.get(slug=slug)
        if request.GET:
            if request.GET['sk'] == user.secretKey:
                try:
                    user.delete()
                    return HttpResponse("Deleted")

                except:
                    return HttpResponse("Unable to delete")
            else:
                return HttpResponse("Wrong Secret Key")
        else:
            template = loader.get_template('people/delete.html')
            context = {'user': user}
            return HttpResponse(template.render(context, request))
    else:
        return redirect('/')


