from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import *

def welcome(request):
	return render(request, 'homepage.html')