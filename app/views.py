#-*- coding: utf-8 -*-	
import os.path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from forms import FileChoosingform
from forms import DataChoosingform
from kmean.normalization import Normalizer
from kmean.kMeanClusterer import KMeanClusterer

def welcome(request):
	return render(request, 'welcome.html')

def result(request):
	return render(request, 'result.html', {'res' : 'pouet', 'fd' : 'null'})

def filechoosing(request):
	if request.method == "POST":
		form = FileChoosingform(request.POST, request.FILES)
		if form.is_valid():
			entete = False
			path = handle_uploaded_file(request.FILES['csvfile'],str(request.FILES['csvfile']))
			if 'entete' in request.POST:
				entete = True
			norm = Normalizer(path, entete)
			request.session['path'] = path
			request.session['entete'] = entete
			request.session['column'] = norm.getCol()
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
	if request.method == "POST":
		form = DataChoosingform(request.POST)
		form.fields['champs'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CHOICES)
		if form.is_valid():
			indexclass = int(form.cleaned_data['index'])
			valueK = int(form.cleaned_data['valueK'])
			valueN = int(form.cleaned_data['valueN'])
			fields = converttab(form.cleaned_data['champs'])
			

			norm = Normalizer(request.session['path'], request.session['entete'])
			res = norm.run(fields, indexclass)
			classes = norm.classes
			kMeanClusterer = KMeanClusterer(res, classes, valueK, valueN)
			jsonres = json.dumps(kMeanClusterer.jsonify())

			request.session['jsondata'] = saveJson(jsonres)
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

def converttab(tab):
	i = 0
	res = []
	for elem in tab:
		res.append(int(elem))
		i = i+1
	return res

def saveData(file, K, N, fields, json):
	data = {}
	data['file']   = file
	data['K']      = K
	data['N']      = N
	data['fields'] = fields
	data['json']   = json
	res = json.dumps(data)
	print res