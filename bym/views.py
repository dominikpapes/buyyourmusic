from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.

def index(request):
    context = {"site_name": "Homepage"}
    return render(request, "bym/index.html", context)