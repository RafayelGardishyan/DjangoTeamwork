from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader

from .models import Short
from .forms import ShortForm


def index(request):
    # if this is a POST request we need to process the form data
    if request.session.get('logged_in'):
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = ShortForm(request.POST)
            # check whether it's valid:
            if form.is_bound:
                if form.is_valid():

                    form.save()

                    template = loader.get_template('error.html')
                    context = {
                        'message': 'Added Short ' + form.cleaned_data['path'] + ' For Url ' + form.cleaned_data['url'],
                        'link': {
                            'text': 'Add another short',
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
        return redirect('/s')
