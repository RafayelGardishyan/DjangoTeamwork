import random

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from .models import People
from Start.models import Admin
from django.core.mail import send_mail
from webhooks import Webhook
# Create your views here.
values = {
    'securitykey': "",
    'whurl': "https://discordapp.com/api/webhooks/399280451258417162/ex_ix9eIhkltscgcS3AyiDt4iVqBpowzAg4LZIFsbuwcJ01jUMkM8Jp78B5YWX6zPoLM",
}

def index(request):
    if request.session.get('logged_in'):
        people = People.objects.filter(activated=True).order_by('name')
        template = loader.get_template('people/index.html')
        context = {
            'people': people,
            'reload': True,
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
            one.activation = "".join([str(random.randint(0, 9)) for i in range(15)])
            one.save()
            template = loader.get_template('error.html')
            context = {
                'message': 'Sent Activation Email to User ' + one.name,
                'link': {
                    'text': 'Return to People home',
                    'url': '/people'
                },
                'slink': {
                    'text': 'Add an other User',
                    'url': '/people/add'
                },
            }
            a = Admin.objects.get(id=1)
            a.sendemail('Added user ' + one.name, 'User secret key: ' + one.secretKey + ' User is not activated yet.')
            send_mail(
                'Email Activation Codeniacs',
                'Hello ' + one.name + '(Sercret Key: ' + one.secretKey +'), Your account is not confirmed. Click on the link to activate: http://codename-codeniacs.herokuapp.com' + one.activationpath() + ' (Testers)',
                'codeniacs@gmail.com',
                [request.GET['e'],],
                fail_silently=False
            )

            embed = Webhook(values['whurl'], color=123123)

            embed.set_author(name='Codeniacs Website',
                             icon='https://codename-codeniacs.herokuapp.com/static/favicon.png')
            embed.set_desc('Added User')
            embed.add_field(name='Name', value=one.name)
            embed.add_field(name='Rank', value=one.rang)
            embed.set_thumbnail('https://codename-codeniacs.herokuapp.com/static/favicon.png')

            embed.set_footer(text='This message was automatically sent form Codeniacs Website',
                             icon='https://codename-codeniacs.herokuapp.com/static/favicon.png', ts=True)
            embed.post()
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
                if request.GET['ak'] == values['securitykey']:
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
                        embed = Webhook(values['whurl'], color=123123)

                        embed.set_author(name='Codeniacs Website',
                                         icon='https://codename-codeniacs.herokuapp.com/static/favicon.png')
                        embed.set_desc('Deleted User')
                        embed.add_field(name='Name', value=username)
                        embed.set_thumbnail('https://codename-codeniacs.herokuapp.com/static/favicon.png')

                        embed.set_footer(text='This message was automatically sent form Codeniacs Website',
                                         icon='https://codename-codeniacs.herokuapp.com/static/favicon.png', ts=True)
                        embed.post()
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
            securitykey = ""
            for i in range(6):
                securitykey += str(random.randint(0, 9))

            print(securitykey)

            admin.sendemail('Delete User', 'Your Security Key is ' + str(securitykey))
            values['securitykey'] = securitykey
            template = loader.get_template('people/delete.html')
            context = {'user': user}
            return HttpResponse(template.render(context, request))
    else:
        return redirect('/')


