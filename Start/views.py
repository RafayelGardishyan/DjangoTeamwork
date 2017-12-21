from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from .models import Admin

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