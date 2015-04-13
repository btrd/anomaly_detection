from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import FileChoosingform
from forms import DataChoosingform
from models import Document
from kmean.normalization import Normalizer

def welcome(request):
	return render(request, 'welcome.html')

def result(request):
	return render(request, 'result.html', {'res' : 'pouet', 'fd' : 'null'})

def filechoosing(request):
	if request.method == "POST":
		form = FileChoosingform(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['csvfile'],"test.csv")
			#norm = Normalizer(request.FILES['csvfile'], False)
			#print norm.getColFloat()
			#extract column name from file
			return HttpResponseRedirect('/datachoosing')
		else:
			return render(request, 'filechoosing.html', {'form' : form})
	else:
		form = FileChoosingform()
		return render(request, 'filechoosing.html', {'form' : form})

def datachoosing(request):
	if request.method == "POST":
		form = DataChoosingform(request.POST)
		if form.is_valid():
			#Do Kmean
			return HttpResponseRedirect('/result')
		else:
			return render(request, 'datachoosing.html', {'form' : form})
	else:
		form = DataChoosingform()
		return render(request, 'datachoosing.html', {'form' : form})

def handle_uploaded_file(file, name):
	destination = open('app/static/documents/'+name, 'w+')
	for chunk in file.chunks():
		destination.write(chunk)
	destination.close()