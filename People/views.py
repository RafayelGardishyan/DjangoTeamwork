from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from .models import People
from Start.models import Admin
from django.core.mail import send_mail
# Create your views here.
def index(request):
    if request.session.get('logged_in'):
        people = People.objects.filter(activated=True).order_by('name')
        template = loader.get_template('people/index.html')
        context = {
            'people': people,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def add(request):
    if request.session.get('logged_in'):
        if 'n' in request.GET:
            one = People()
            one.name = request.GET['n']
            one.birthDate = request.GET['bd']
            one.rang = request.GET['r']
            one.secretKey = request.GET['sk']
            one.saveslug(request.GET['n'])
            one.save()
            template = loader.get_template('error.html')
            context = {
                'message': 'Added User ' + one.name,
                'link': {
                    'text': 'Return to People home',
                    'url': '/people'
                }
            }
            send_mail(
                'Email Activation Codeniacs',
                'Your account is not confirmed. Click on the link to activate: http://127.0.0.1:8000' + one.activationpath() + ' (Testers)',
                'codeniacs@gmail.com',
                [request.GET['e'],],
                fail_silently=False
            )
            return HttpResponse(template.render(context, request))
        else:
            context = {'message': "Add new users"}
            template = loader.get_template('people/add.html')
            return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def delete(request, slug):
    if request.session.get('logged_in'):
        user = People.objects.get(slug=slug)
        admin = Admin.objects.get(id=1)
        if request.GET:
            if request.GET['sk'] == user.secretKey:
                if request.GET['ak'] == admin.password:
                    try:
                        username = user.name
                        user.delete()
                        template = loader.get_template('error.html')
                        context = {
                            'message': 'Deleted User ' + username,
                            'link': {
                                'text': 'Return to People home',
                                'url': '/people'
                            }
                        }
                        return HttpResponse(template.render(context, request))

                    except:
                        template = loader.get_template('error.html')
                        context = {
                            'message': 'Unable to delete',
                            'link': {
                                'text': 'Return to People home',
                                'url': '/people'
                            }
                        }
                        return HttpResponse(template.render(context, request))
                else:
                    template = loader.get_template('error.html')
                    context = {
                        'message': 'Wrong Admin Key',
                        'link': {
                            'text': 'Return to People home',
                            'url': '/people'
                        }
                    }
                    return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('error.html')
                context = {
                    'message': 'Wrong Secret Key',
                    'link': {
                        'text': 'Return to People home',
                        'url': '/people'
                    }
                }
                return HttpResponse(template.render(context, request))
        else:
            template = loader.get_template('people/delete.html')
            context = {'user': user}
            return HttpResponse(template.render(context, request))
    else:
        return redirect('/')


