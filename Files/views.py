from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from Start.models import Admin

from .forms import FileForm
from .models import File
# Create your views here.
def index(request):
    if request.session.get('logged_in'):
        files = File.objects.order_by('added_on')
        template = loader.get_template('files/index.html')
        context = {
            'files': files,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def delete(request, slug):
    if request.session.get('logged_in'):
       file = File.objects.get(slug=slug)
       filename = file.name
       user = Admin.objects.get(name="Rafayel Gardishyan")
       if request.GET:
           if request.GET['ak'] == user.secretKey:
               file.deletefile()
               file.delete()
               template = loader.get_template('error.html')
               context = {
                   'message': 'Successfully deleted file ' + filename,
                   'link': {
                       'text': 'Return to Files home',
                       'url': '/files'
                   }
               }
               return HttpResponse(template.render(context, request))
           else:
               template = loader.get_template('error.html')
               context = {
                   'message': 'Wrong Admin Key',
                   'link': {
                       'text': 'Return to Files home',
                       'url': '/files'
                   }
               }
               return HttpResponse(template.render(context, request))

       else:
           template = loader.get_template('files/delete.html')
           context = {}
           return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def add(request):
    # if this is a POST request we need to process the form data
    if request.session.get('logged_in'):
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = FileForm(request.POST, files=request.FILES)
            # check whether it's valid:
            if form.is_bound:
                if form.is_valid():
                    form.save()

                    template = loader.get_template('error.html')
                    context = {
                        'message': 'Added File ' + form.file.name,
                        'link': {
                            'text': 'Return to Files home',
                            'url': '/files',
                        }
                    }
                    return HttpResponse(template.render(context, request))
                else:
                    template = loader.get_template('error.html')
                    context = {
                        'message': 'Form is not valid',
                        'link': {
                            'text': 'Return to Files home',
                            'url': '/files'
                        }
                    }
                    return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('error.html')
                context = {
                    'message': 'Form is not bound',
                    'link': {
                        'text': 'Return to Files home',
                        'url': '/files'
                    }
                }
                return HttpResponse(template.render(context, request))

        # if a GET (or any other method) we'll create a blank form
        else:
            form = FileForm()
            template = loader.get_template('plans/add.html')
            context = {'form': form}
            return HttpResponse(template.render(context, request))
    else:
        return redirect('/')
