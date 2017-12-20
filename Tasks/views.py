from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect

from .models import Task
from People.models import People
from .forms import TaskForm
# Create your views here.
def index(request):
    tasks = Task.objects.order_by('name')
    template = loader.get_template('tasks/index.html')
    context = {
        'tasks': tasks,
    }
    return HttpResponse(template.render(context, request))

def add(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TaskForm(request.POST)
        # check whether it's valid:
        if form.is_bound:
            if form.is_valid():

                form.save()

                return HttpResponse("<a href=\"/\"> Go to homepage </a>")

            else:
                return HttpResponse("Form not valid")
        else:
            return HttpResponse("Form is not bound")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TaskForm()
        template = loader.get_template('tasks/add.html')
        context = {'form': form}
        return HttpResponse(template.render(context, request))

def delete(request, slug):
    task = Task.objects.get(slug=slug)
    taskname = task.name
    user = task.user
    if request.GET:
        if request.GET['sk'] == user.secretKey:
            task.delete()
            return HttpResponse("Successfully deleted task " + taskname)
        else:
            return HttpResponse("Wrong Secret Key")
    else:
        template = loader.get_template('tasks/delete.html')
        context = {
            'user': user
        }
        return HttpResponse(template.render(context, request))
