import random
import string

import sys

import os
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from .models import Admin
from People.models import People

values = {
    'licensekey' : ''
}

def index(request):
    try:
        admin = Admin.objects.get(id=1)
    except:
        return redirect('/activate')
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

def activate(request, slug, rang, sk, ac):
    try:
        user = People.objects.get(slug=slug)
    except:
        template = loader.get_template('error.html')
        context = {
            'message': 'User does not exist',
            'link': {
                'url': '/',
                'text': 'Return to start page'
            }
        }
        return HttpResponse(template.render(context, request))
    if user.rang == rang:
        if user.secretKey == sk:
            if user.activation == ac:
                user.activated = True
                user.save()
                a = Admin.objects.get(id=1)
                a.sendemail('Activated user', 'Activated user ' + user.name)
                return redirect('/')
            else:
                template = loader.get_template('error.html')
                context = {
                    'message': 'Wrong Activation Code',
                    'link': {
                        'url': '/',
                        'text': 'Return to start page'
                    }
                }
                return HttpResponse(template.render(context, request))
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
    if request.GET:
        try:
            if Admin.objects.get(id=1):
                return redirect('/')
        except:
            if request.GET['lk'] != values['licensekey']:
                return redirect('/activate')
            a = Admin()
            a.password = request.GET['pw']
            a.email = request.GET['e']
            a.license = request.GET['lk']
            a.save()
            return redirect('/')
    else:
        values['licensekey'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        send_mail('License Key For Django Team Website', 'License Key: ' + values['licensekey'], 'codeniacs@gmail.com', [os.environ.get('SUPERADMINDJTWE',)], fail_silently=False)
        template = loader.get_template('start/websiteactivation.html')
        context = {}
        return HttpResponse(template.render(context, request))
