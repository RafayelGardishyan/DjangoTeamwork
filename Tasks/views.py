import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponseRedirect

from Start.models import Admin
from .models import Task, CompletedTask
from People.models import People
from .forms import TaskForm
from webhooks import Webhook



# Create your views here.

values = {
    'securitykey': "",
    'whurl': "https://discordapp.com/api/webhooks/399280451258417162/ex_ix9eIhkltscgcS3AyiDt4iVqBpowzAg4LZIFsbuwcJ01jUMkM8Jp78B5YWX6zPoLM",
}

def index(request):
    if request.session.get('logged_in'):
        if request.GET.get('reload'):
            reload = bool(request.GET.get('reload'))
        else:
            reload = True
        completed = len(CompletedTask.objects.filter())
        inprogress = len(Task.objects.filter(inprogress=True))
        other = len(Task.objects.filter(inprogress=False))
        if completed == 0 and inprogress == 0 and other == 0:
            status = 'link'
        elif completed > (inprogress + other):
            status = 'greenlinks'
        elif completed < (inprogress +other):
            status = 'redlinks'
        else:
            status = 'orangelinks'
        tasks = Task.objects.order_by('date')
        template = loader.get_template('tasks/index.html')
        context = {
            'status': status,
            'tasks': tasks,
            'reload': reload,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def indexCompleted(request):
    if request.session.get('logged_in'):
        if request.GET.get('reload'):
            reload = bool(request.GET.get('reload'))
        else:
            reload = True
        completed = len(CompletedTask.objects.filter())
        inprogress = len(Task.objects.filter(inprogress=True))
        other = len(Task.objects.filter(inprogress=False))
        if completed == 0 and inprogress == 0 and other == 0:
            status = 'link'
        elif completed > (inprogress + other):
            status = 'greenlinks'
        elif completed < (inprogress +other):
            status = 'redlinks'
        else:
            status = 'orangelinks'
        tasks = CompletedTask.objects.order_by('completed_on')
        template = loader.get_template('tasks/indexC.html')
        context = {
            'tasks': tasks,
            'status': status,
            'reload': reload,
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
                        },
                        'slink': {
                            'text': 'Add an other Task',
                            'url': '/tasks/add'
                        },
                    }

                    embed = Webhook(values['whurl'], color=123123)

                    embed.set_author(name='Codeniacs Website', icon='https://codename-codeniacs.herokuapp.com/static/favicon.png')
                    embed.set_desc('Added new Task for user ' + form.cleaned_data['user'].name)
                    embed.add_field(name='Name', value=form.cleaned_data['name'])
                    embed.add_field(name='Deadline', value=str(form.cleaned_data['date']))
                    embed.set_thumbnail('https://codename-codeniacs.herokuapp.com/static/favicon.png')

                    embed.set_footer(text='This message was automatically sent form Codeniacs Website', icon='https://codename-codeniacs.herokuapp.com/static/favicon.png', ts=True)
                    embed.post()
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
               embed = Webhook(values['whurl'], color=123123)

               embed.set_author(name='Codeniacs Website',
                                icon='https://codename-codeniacs.herokuapp.com/static/favicon.png')
               embed.set_desc('Completed Task')
               embed.add_field(name='Name', value=taskname)
               embed.set_thumbnail('https://codename-codeniacs.herokuapp.com/static/favicon.png')

               embed.set_footer(text='This message was automatically sent form Codeniacs Website',
                                icon='https://codename-codeniacs.herokuapp.com/static/favicon.png', ts=True)
               embed.post()
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
        embed = Webhook(values['whurl'], color=123123)

        embed.set_author(name='Codeniacs Website',
                         icon='https://codename-codeniacs.herokuapp.com/static/favicon.png')
        embed.set_desc('Task in progress')
        embed.add_field(name='Name', value=task.name)
        embed.set_thumbnail('https://codename-codeniacs.herokuapp.com/static/favicon.png')
        embed.set_footer(text='This message was automatically sent form Codeniacs Website',
                         icon='https://codename-codeniacs.herokuapp.com/static/favicon.png', ts=True)
        embed.post()
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
        completed = len(CompletedTask.objects.filter())
        inprogress = len(Task.objects.filter(inprogress=True))
        other = len(Task.objects.filter(inprogress=False))
        if completed == 0 and inprogress == 0 and other == 0:
            status = 'link'
        elif completed > (inprogress + other):
            status = 'greenlinks'
        elif completed < (inprogress +other):
            status = 'redlinks'
        else:
            status = 'orangelinks'
        if not request.GET:
            users = People.objects.order_by('name')
            template = loader.get_template('tasks/filteruser.html')
            context = {
                'users': users,
            }
            return HttpResponse(template.render(context, request))
        else:
            if request.GET.get('reload'):
                reload = bool(request.GET.get('reload'))
            else:
                reload = True
            tasks = Task.objects.filter(user=request.GET['user'])
            template = loader.get_template('tasks/index.html')
            context = {
                'tasks': tasks,
                'status': status,
                'reload': reload,
            }
            return HttpResponse(template.render(context, request))

    else:
        return redirect('/')

def filterdate(request):
    if request.session.get('logged_in'):
        completed = len(CompletedTask.objects.filter())
        inprogress = len(Task.objects.filter(inprogress=True))
        other = len(Task.objects.filter(inprogress=False))
        if completed == 0 and inprogress == 0 and other == 0:
            status = 'link'
        elif completed > (inprogress + other):
            status = 'greenlinks'
        elif completed < (inprogress +other):
            status = 'redlinks'
        else:
            status = 'orangelinks'
        if not request.GET:
            template = loader.get_template('tasks/filterdate.html')
            context = {}
            return HttpResponse(template.render(context, request))
        else:
            if request.GET.get('reload'):
                reload = bool(request.GET.get('reload'))
            else:
                reload = True
            tasks = Task.objects.filter(date=request.GET['date'])
            template = loader.get_template('tasks/index.html')
            context = {
                'tasks': tasks,
                'status': status,
                'reload': reload,
            }
            return HttpResponse(template.render(context, request))

    else:
        return redirect('/')

def stats(request):
    if request.session.get('logged_in'):
        if request.GET.get('reload'):
            reload = bool(request.GET.get('reload'))
        else:
            reload = True
        completed = len(CompletedTask.objects.filter())
        inprogress = len(Task.objects.filter(inprogress=True))
        other = len(Task.objects.filter(inprogress=False))
        print(reload)
        context = {
            'completed': completed,
            'inprogress': inprogress,
            'tasks': other,
            'reload': reload,
        }
        template = loader.get_template('tasks/stats.html')
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')
