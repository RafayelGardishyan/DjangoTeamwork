import random

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader


from Start.models import Admin
from .forms import PlanForm
from .models import Plan
# Create your views here.
values = {
    'securitytkey': ""
}

def index(request):
    if request.session.get('logged_in'):
        plans = Plan.objects.order_by('deadline')
        template = loader.get_template('plans/index.html')
        context = {
            'plans': plans,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def add(request):
    # if this is a POST request we need to process the form data
    if request.session.get('logged_in'):
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = PlanForm(request.POST)
            # check whether it's valid:
            if form.is_bound:
                if form.is_valid():

                    form.save()

                    template = loader.get_template('error.html')
                    context = {
                        'message': 'Added Plan ' + form.cleaned_data['name'],
                        'link': {
                            'text': 'Return to Plans home',
                            'url': '/plans',
                        }
                    }
                    return HttpResponse(template.render(context, request))
                else:
                    template = loader.get_template('error.html')
                    context = {
                        'message': 'Form is not valid',
                        'link': {
                            'text': 'Return to Plans home',
                            'url': '/plans'
                        }
                    }
                    return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('error.html')
                context = {
                    'message': 'Form is not bound',
                    'link': {
                        'text': 'Return to Plans home',
                        'url': '/plans'
                    }
                }
                return HttpResponse(template.render(context, request))

        # if a GET (or any other method) we'll create a blank form
        else:
            form = PlanForm()
            template = loader.get_template('plans/add.html')
            context = {'form': form}
            return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def delete(request, slug):
    if request.session.get('logged_in'):
       task = Plan.objects.get(slug=slug)
       planname = task.name
       user = Admin.objects.get(id=1)
       if request.GET:
           if request.GET['ak'] == values['securitytkey']:
               task.delete()
               template = loader.get_template('error.html')
               context = {
                   'message': 'Successfully deleted plan ' + planname,
                   'link': {
                       'text': 'Return to Plans home',
                       'url': '/plans'
                   }
               }
               return HttpResponse(template.render(context, request))
           else:
               template = loader.get_template('error.html')
               context = {
                   'message': 'Wrong Admin Key',
                   'link': {
                       'text': 'Return to Plans home',
                       'url': '/plans'
                   }
               }
               return HttpResponse(template.render(context, request))

       else:
           securitykey = ""
           for i in range(6):
               securitykey += str(random.randint(0, 9))

           print(securitykey)

           user.sendemail('Delete Plan', 'Your Security Key is ' + str(securitykey))
           values['securitykey'] = securitykey
           template = loader.get_template('plans/delete.html')
           context = {}
           return HttpResponse(template.render(context, request))
    else:
        return redirect('/')

def description(request, slug):
    if request.session.get('logged_in'):
        plan = Plan.objects.get(slug=slug)
        template = loader.get_template('plans/description.html')
        context = {
            'plan': plan,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')