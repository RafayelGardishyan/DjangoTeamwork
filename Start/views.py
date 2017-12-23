from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from .models import Admin
from People.models import People

def index(request):
    admin = Admin.objects.get(id=1)
    if not request.session.get('logged_in'):
        if request.GET:
            if request.GET['pw'] == admin.password:
                request.session['logged_in'] = True
                return redirect("/tasks")
            else:
                template = loader.get_template('start/start.html')
                context = {}
                return HttpResponse(template.render(context, request))
        else:
            template = loader.get_template('start/start.html')
            context = {}
            return HttpResponse(template.render(context, request))
    else:
        return redirect('/tasks')

def delete(request):
    try:
        del request.session['logged_in']
        return redirect('/')
    except:
        return redirect('/')

def activate(request, slug, rang, sk):
    user = People.objects.get(slug=slug)
    if user.rang == rang:
        if user.secretKey == sk:
            user.activated = True
            user.save()
            return redirect('/')
        else:
            template = loader.get_template('error.html')
            context = {
                'message': 'Wrong Secret Key. Account not activated',
                'link': {
                    'url': '/',
                    'text': 'Return to start page'
                }
            }
            return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('error.html')
        context = {
            'message': 'Wrong Rank. Account not activated',
            'link': {
                'url': '/',
                'text': 'Return to start page'
            }
        }
        return HttpResponse(template.render(context, request))

def siteact(request):
    if not Admin.objects.get(id=1):
        a = Admin()
        a.password = 'Cod3niacs2018!'
        a.save()
    return redirect('/')
