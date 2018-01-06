import random

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader


from Start.models import Admin
from .forms import IdeaForm
from .models import Idea
from webhooks import Webhook
# Create your views here.
values = {
    'securitykey': "",
    'whurl': "https://discordapp.com/api/webhooks/399280451258417162/ex_ix9eIhkltscgcS3AyiDt4iVqBpowzAg4LZIFsbuwcJ01jUMkM8Jp78B5YWX6zPoLM",
}
def index(request):
    if request.session.get('logged_in'):
        ideas = Idea.objects.order_by('name')
        template = loader.get_template('ideas/index.html')
        context = {
            'ideas': ideas,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def add(request):
    # if this is a POST request we need to process the form data
    if request.session.get('logged_in'):
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = IdeaForm(request.POST)
            # check whether it's valid:
            if form.is_bound:
                if form.is_valid():

                    form.save()

                    template = loader.get_template('error.html')
                    context = {
                        'message': 'Added Idea ' + form.cleaned_data['title'],
                        'link': {
                            'text': 'Return to Ideas home',
                            'url': '/ideas',
                        },
                        'slink': {
                            'text': 'Add an other Idea',
                            'url': '/ideas/add'
                        },
                    }
                    embed = Webhook(values['whurl'], color=123123)

                    embed.set_author(name='Codeniacs Website',
                                     icon='https://codename-codeniacs.herokuapp.com/static/favicon.png')
                    embed.set_desc('Added Idea')
                    embed.add_field(name='Name', value=form.cleaned_data['title'])
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
                            'text': 'Return to Ideas home',
                            'url': '/ideas'
                        }
                    }
                    return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('error.html')
                context = {
                    'message': 'Form is not bound',
                    'link': {
                        'text': 'Return to Ideas home',
                        'url': '/ideas'
                    }
                }
                return HttpResponse(template.render(context, request))

        # if a GET (or any other method) we'll create a blank form
        else:
            form = IdeaForm()
            template = loader.get_template('ideas/add.html')
            context = {'form': form}
            return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def delete(request, slug):
    if request.session.get('logged_in'):
       idea = Idea.objects.get(slug=slug)
       ideaname = idea.name
       user = Admin.objects.get(id=1)

       if request.GET:
           if request.GET['sk'] == values['securitykey']:
               idea.delete()
               template = loader.get_template('error.html')
               context = {
                   'message': 'Successfully deleted idea ' + ideaname,
                   'link': {
                       'text': 'Return to Ideas home',
                       'url': '/ideas'
                   }
               }
               embed = Webhook(values['whurl'], color=123123)

               embed.set_author(name='Codeniacs Website',
                                icon='https://codename-codeniacs.herokuapp.com/static/favicon.png')
               embed.set_desc('Deleted Idea')
               embed.add_field(name='Name', value=ideaname)
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
                       'text': 'Return to Ideas home',
                       'url': '/ideas'
                   }
               }
               return HttpResponse(template.render(context, request))

       else:
           securitykey = ""
           for i in range(6):
               securitykey += str(random.randint(0, 9))

           print(securitykey)

           user.sendemail('Delete Idea', 'Your Security Key is ' + str(securitykey))
           values['securitykey'] = securitykey
           template = loader.get_template('ideas/delete.html')
           context = {}
           return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def description(request, slug):
    if request.session.get('logged_in'):
        idea = Idea.objects.get(slug=slug)
        template = loader.get_template('ideas/description.html')
        context = {
            'idea': idea,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')