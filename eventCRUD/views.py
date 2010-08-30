from django.views.generic.simple import direct_to_template, HttpResponseRedirect
from django.views.generic.list_detail import object_detail
from django.views.generic import list_detail
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from django.shortcuts import get_object_or_404, render_to_response

from eventCRUD.forms import LarpForm, RunForm


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/home")
    else:
        form = UserCreationForm()
    c = {}
    c.update(csrf(request))
    return render_to_response("registration/register.html", {
        'form': form,
    }
    ,
    context_instance=RequestContext(request))