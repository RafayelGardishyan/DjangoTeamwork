import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponseRedirect

from Start.models import Admin
from .models import Task, CompletedTask
from People.models import People
from .forms import TaskForm
# Create your views here.

values = {
    'securitykey': ""
}

def index(request):
    if request.session.get('logged_in'):
        tasks = Task.objects.order_by('date')
        template = loader.get_template('tasks/index.html')
        context = {
            'tasks': tasks,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def indexCompleted(request):
    if request.session.get('logged_in'):
        tasks = CompletedTask.objects.order_by('completed_on')
        template = loader.get_template('tasks/indexC.html')
        context = {
            'tasks': tasks,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def add(request):
    # if this is a POST request we need to process the form data
    if request.session.get('logged_in'):
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = TaskForm(request.POST)
            # check whether it's valid:
            if form.is_bound:
                if form.is_valid():

                    form.save()

                    template = loader.get_template('error.html')
                    context = {
                        'message': 'Added Task ' + form.cleaned_data['name'] + ' For User ' + form.cleaned_data['user'].name,
                        'link': {
                            'text': 'Return to Tasks home',
                            'url': '/tasks'
                        }
                    }
                    return HttpResponse(template.render(context, request))
                else:
                    template = loader.get_template('error.html')
                    context = {
                        'message': 'Form is not valid',
                        'link': {
                            'text': 'Return to Tasks home',
                            'url': '/tasks'
                        }
                    }
                    return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('error.html')
                context = {
                    'message': 'Form is not bound',
                    'link': {
                        'text': 'Return to Tasks home',
                        'url': '/tasks'
                    }
                }
                return HttpResponse(template.render(context, request))

        # if a GET (or any other method) we'll create a blank form
        else:
            form = TaskForm()
            template = loader.get_template('tasks/add.html')
            context = {'form': form}
            return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def delete(request, slug):
    if request.session.get('logged_in'):
       task = Task.objects.get(slug=slug)
       taskname = task.name
       user = task.user
       if request.GET:
           if request.GET['sk'] == user.secretKey:
               ctask = CompletedTask()
               ctask.name = task.name
               ctask.date = task.date
               ctask.user = task.user
               ctask.saveslug(ctask.name)
               ctask.save()
               task.delete()
               template = loader.get_template('error.html')
               context = {
                   'message': 'Successfully deleted task ' + taskname,
                   'link': {
                       'text': 'Return to Tasks home',
                       'url': '/tasks'
                   }
               }
               return HttpResponse(template.render(context, request))
           else:
               template = loader.get_template('error.html')
               context = {
                   'message': 'Wrong Secret Key',
                   'link': {
                       'text': 'Return to Tasks home',
                       'url': '/tasks'
                   }
               }
               return HttpResponse(template.render(context, request))
       else:
           template = loader.get_template('tasks/delete.html')
           context = {
               'user': user
           }
           return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def progress(request, slug):
    if request.session.get('logged_in'):
        task = Task.objects.get(slug=slug)
        task.inprogress = True
        task.save()
        return redirect('/tasks')
    else:
        return redirect('/')

def deleteCompleted(request, slug):
    if request.session.get('logged_in'):
        task = CompletedTask.objects.get(slug=slug)
        taskname = task.name
        user = Admin.objects.get(id=1)
        if request.GET:
            if request.GET['sk'] == values['securitykey']:
                task.delete()
                template = loader.get_template('error.html')
                context = {
                    'message': 'Successfully deleted task ' + taskname,
                    'link': {
                        'text': 'Return to Completed Tasks home',
                        'url': '/tasks/completed'
                    }
                }
                return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('error.html')
                context = {
                    'message': 'Wrong Secret Key',
                    'link': {
                        'text': 'Return to Completed Tasks home',
                        'url': '/tasks/completed'
                    }
                }
                return HttpResponse(template.render(context, request))
        else:
            securitykey = ""
            for i in range(6):
                securitykey += str(random.randint(0, 9))

            print(securitykey)

            user.sendemail('Delete Completed Task', 'Your Security Key is ' + str(securitykey))
            values['securitykey'] = securitykey
            template = loader.get_template('tasks/deleteC.html')
            context = {
                'user': user
            }
            return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def filteruser(request):
    if request.session.get('logged_in'):
        if not request.GET:
            users = People.objects.order_by('name')
            template = loader.get_template('tasks/filteruser.html')
            context = {
                'users': users,
            }
            return HttpResponse(template.render(context, request))
        else:
            tasks = Task.objects.filter(user=request.GET['user'])
            template = loader.get_template('tasks/index.html')
            context = {
                'tasks': tasks,
            }
            return HttpResponse(template.render(context, request))

    else:
        return redirect('/')

def filterdate(request):
    if request.session.get('logged_in'):
        if not request.GET:
            template = loader.get_template('tasks/filterdate.html')
            context = {}
            return HttpResponse(template.render(context, request))
        else:
            tasks = Task.objects.filter(date=request.GET['date'])
            template = loader.get_template('tasks/index.html')
            context = {
                'tasks': tasks,
            }
            return HttpResponse(template.render(context, request))

    else:
        return redirect('/')
