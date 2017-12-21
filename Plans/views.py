from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from .models import Plan
# Create your views here.
def index(request):
    if request.session.get('logged_in'):
        plans = Plan.objects.order_by('name')
        template = loader.get_template('plans/index.html')
        context = {
            'plans': plans,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')