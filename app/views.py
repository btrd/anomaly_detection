#-*- coding: utf-8 -*-	
import os.path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from forms import FileChoosingform
from forms import DataChoosingform
from kmean.normalization import Normalizer

def welcome(request):
	return render(request, 'welcome.html')

def result(request):
	return render(request, 'result.html', {'res' : 'pouet', 'fd' : 'null'})

def filechoosing(request):
	if request.method == "POST":
		form = FileChoosingform(request.POST, request.FILES)
		if form.is_valid():
			print 
			path = handle_uploaded_file(request.FILES['csvfile'],str(request.FILES['csvfile']))
			#norm = Normalizer(path, False)
			#print norm.getColFloat()
			request.session['column'] = ["pouet","foo","bar"]
			if 'entete' in request.POST:
				print('entete présente')
			#extract column name from file
			return HttpResponseRedirect('/datachoosing')
		else:
			return render(request, 'filechoosing.html', {'form' : form})
	else:
		form = FileChoosingform()
		return render(request, 'filechoosing.html', {'form' : form})

def datachoosing(request):
	if 'column' in request.session:
		CHOICES = buildtuple(request.session['column'])
	else:
		return HttpResponseRedirect('/filechoosing')
	#CHOICES = (("0", "column0"),("1", "column1"),("2", "column2"),("3", "column3"))
	if request.method == "POST":
		form = DataChoosingform(request.POST)
		form.fields['champs'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CHOICES)
		if form.is_valid():
			#Do Kmean
			return HttpResponseRedirect('/result')
		else:
			return render(request, 'datachoosing.html', {'form' : form})
	else:
		form = DataChoosingform()
		form.fields['champs'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CHOICES)
		return render(request, 'datachoosing.html', {'form' : form})

def handle_uploaded_file(file, name):
	path = 'app/static/documents/' + name
	if not os.path.isfile(path):
		destination = open(path, 'w+')
		for chunk in file.chunks():
			destination.write(chunk)
		destination.close()
	else:
		print("File already on server, abord upload")
	return path


def buildtuple(tab):
	i = 0
	res = []
	for elem in tab:
		res.append((i, elem))
		i = i+1
	return res