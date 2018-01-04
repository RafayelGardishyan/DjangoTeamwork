from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader


def index(request):
    if request.session.get('logged_in'):
        template = loader.get_template('calendar/index.html')
        context = {

        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')
