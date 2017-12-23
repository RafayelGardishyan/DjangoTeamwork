from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from .models import Log
from .forms import LogForm
# Create your views here.
def index(request):
    if request.session.get('logged_in'):
        logs = Log.objects.order_by('added')
        template = loader.get_template('logs/index.html')
        context = {
            'logs': logs,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def add(request):
    # if this is a POST request we need to process the form data
    if request.session.get('logged_in'):
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = LogForm(request.POST)
            # check whether it's valid:
            if form.is_bound:
                if form.is_valid():

                    form.save()

                    template = loader.get_template('error.html')
                    context = {
                        'message': 'Added Logs ' + form.cleaned_data['title'] + ' By user ' + form.cleaned_data['user'].name,
                        'link': {
                            'text': 'Return to Logs home',
                            'url': '/logs',
                        }
                    }
                    return HttpResponse(template.render(context, request))
                else:
                    template = loader.get_template('error.html')
                    context = {
                        'message': 'Form is not valid',
                        'link': {
                            'text': 'Return to Logs home',
                            'url': '/logs'
                        }
                    }
                    return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('error.html')
                context = {
                    'message': 'Form is not bound',
                    'link': {
                        'text': 'Return to Logs home',
                        'url': '/logs'
                    }
                }
                return HttpResponse(template.render(context, request))

        # if a GET (or any other method) we'll create a blank form
        else:
            form = LogForm()
            template = loader.get_template('logs/add.html')
            context = {'form': form}
            return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def delete(request, slug):
    if request.session.get('logged_in'):
       log = Log.objects.get(slug=slug)
       logname = log.title
       user = log.user
       if request.GET:
           if request.GET['sk'] == user.secretKey:
               log.delete()
               template = loader.get_template('error.html')
               context = {
                   'message': 'Successfully deleted log ' + logname,
                   'link': {
                       'text': 'Return to Logs home',
                       'url': '/logs'
                   }
               }
               return HttpResponse(template.render(context, request))
           else:
               template = loader.get_template('error.html')
               context = {
                   'message': 'Wrong Secret Key',
                   'link': {
                       'text': 'Return to Logs home',
                       'url': '/logs'
                   }
               }
               return HttpResponse(template.render(context, request))
       else:
           template = loader.get_template('logs/delete.html')
           context = {
               'user': user
           }
           return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def view(request, slug):
    if request.session.get('logged_in'):
        log = Log.objects.get(slug=slug)
        template = loader.get_template('logs/view.html')
        context = {
            'log': log,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')
