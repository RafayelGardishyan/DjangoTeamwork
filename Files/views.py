import random

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from Start.models import Admin

from .forms import FileForm
from .models import File
from webhooks import Webhook
# Create your views here.
values = {
    'securitykey': "",
    'whurl': "https://discordapp.com/api/webhooks/399280451258417162/ex_ix9eIhkltscgcS3AyiDt4iVqBpowzAg4LZIFsbuwcJ01jUMkM8Jp78B5YWX6zPoLM",
}

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
       user = Admin.objects.get(id=1)
       if request.GET:
           if request.GET['ak'] == values['securitykey']:
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
               embed = Webhook(values['whurl'], color=123123)

               embed.set_author(name='Codeniacs Website',
                                icon='https://codename-codeniacs.herokuapp.com/static/favicon.png')
               embed.set_desc('Deleted File')
               embed.add_field(name='Name', value=filename)
               embed.set_thumbnail('https://codename-codeniacs.herokuapp.com/static/favicon.png')
               embed.set_footer(text='This message was automatically sent form Codeniacs Website',
                                icon='https://codename-codeniacs.herokuapp.com/static/favicon.png', ts=True)
               embed.post()
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
           securitykey = ""
           for i in range(6):
               securitykey += str(random.randint(0, 9))

           print(securitykey)

           user.sendemail('Delete File', 'Your Security Key is ' + str(securitykey))
           values['securitykey'] = securitykey
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
                        'message': 'Added File',
                        'link': {
                            'text': 'Return to Files home',
                            'url': '/files',
                        },
                        'slink': {
                            'text': 'Add an other File',
                            'url': '/files/add'
                        },
                    }
                    embed = Webhook(values['whurl'], color=123123)

                    embed.set_author(name='Codeniacs Website',
                                     icon='https://codename-codeniacs.herokuapp.com/static/favicon.png')
                    embed.set_desc('Added File')
                    embed.add_field(name='Name', value=form.cleaned_data['file'])
                    embed.set_thumbnail('https://codename-codeniacs.herokuapp.com/static/favicon.png')
                    embed.set_footer(text='This message was automatically sent form Codeniacs Website',
                                     icon='https://codename-codeniacs.herokuapp.com/static/favicon.png', ts=True)
                    embed.post()
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
            template = loader.get_template('files/add.html')
            context = {'form': form}
            return HttpResponse(template.render(context, request))
    else:
        return redirect('/')
