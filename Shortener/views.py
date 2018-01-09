from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
import requests as rq
from .models import Short
from .forms import ShortForm
from webhooks import Webhook

values = {
    'whurl': "https://discordapp.com/api/webhooks/399280451258417162/ex_ix9eIhkltscgcS3AyiDt4iVqBpowzAg4LZIFsbuwcJ01jUMkM8Jp78B5YWX6zPoLM"
}

def index(request):
    # if this is a POST request we need to process the form data
    if request.session.get('logged_in'):
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = ShortForm(request.POST)
            # check whether it's valid:

            if form.is_bound:
                if form.is_valid():
                    shorts = Short.objects.all()
                    exists = False
                    for short in shorts:
                        if short.slug == form.cleaned_data['path']:
                            exists = True
                    if not exists:
                        form.save()

                        template = loader.get_template('error.html')
                        context = {
                            'message': 'Added Short codename-codeniacs.herokuapp.com/s/' + form.cleaned_data['path'] + ' For Url ' + form.cleaned_data['url'],
                            'link': {
                                'text': 'Add another short',
                                'url': '/s'
                            },
                            'slink': {
                                'text': 'Visit Website',
                                'url': form.cleaned_data['url']
                            },
                        }
                        embed = Webhook(values['whurl'], color=123123)

                        embed.set_author(name='Codeniacs Website',
                                         icon='https://codename-codeniacs.herokuapp.com/static/favicon.png')
                        embed.set_desc('Added Shortcut')
                        embed.add_field(name='Path', value=form.cleaned_data['path'])
                        embed.add_field(name='Url', value=form.cleaned_data['url'])
                        embed.set_thumbnail('https://codename-codeniacs.herokuapp.com/static/favicon.png')

                        embed.set_footer(text='This message was automatically sent form Codeniacs Website',
                                         icon='https://codename-codeniacs.herokuapp.com/static/favicon.png', ts=True)
                        embed.post()
                        return HttpResponse(template.render(context, request))
                    else:
                        template = loader.get_template('error.html')
                        context = {
                            'message': 'Short already exists',
                            'link': {
                                'text': 'Try again',
                                'url': '/s'
                            }
                        }
                        return HttpResponse(template.render(context, request))
                else:
                    template = loader.get_template('error.html')
                    context = {
                        'message': 'Form is not valid',
                        'link': {
                            'text': 'Return to Shortener home',
                            'url': '/s'
                        }
                    }
                    return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('error.html')
                context = {
                    'message': 'Form is not bound',
                    'link': {
                        'text': 'Return to Shortener home',
                        'url': '/s'
                    }
                }
                return HttpResponse(template.render(context, request))

        # if a GET (or any other method) we'll create a blank form
        else:
            form = ShortForm()
            template = loader.get_template('shortener/add.html')
            context = {'form': form}
            return HttpResponse(template.render(context, request))
    else:
        return redirect('/')


def redirectUrl(request, slug):
    try:
        short = Short.objects.get(slug=slug)
        return redirect(short.link)
    except:
        return redirect('/s/')
