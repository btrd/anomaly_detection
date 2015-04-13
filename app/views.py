#-*- coding: utf-8 -*-	
import json
import time
import os
from os import listdir
from os.path import isfile, join
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from forms import FileChoosingform
from forms import DataChoosingform
from forms import OldResultForm
from kmean.normalization import Normalizer
from kmean.kMeanClusterer import KMeanClusterer

def result(request):
	if 'file' in request.GET:
		path = str(request.GET['file'])
		print path
		with open(path) as data_file:
			print data_file
			data = json.load(data_file)
			return render(request, 'result.html', {'filename' : data['file'],
													 'K' : data['K'],
													 'N' : data['N'],
													 'fields' : data['fields'],
													 'json' : str(data['json'])})
	return HttpResponseRedirect('/')

def filechoosing(request):
	CHOICES = getallsavedJson()
	if request.method == "POST":
		if 'oldresult' not in request.POST: #gestion du formulaire FileChoosing
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
				return HttpResponseRedirect('/datachoosing')
			else:
				form_results = OldResultForm()
				form_results.fields['oldresult'].choices = CHOICES
				return render(request, 'filechoosing.html', {'form' : form, 'form_results' : form_results})
		else: #Gestion du formulaire Oldresult
			form_results = OldResultForm(request.POST)
			form_results.fields['oldresult'].choices = CHOICES
			if form_results.is_valid():
				jsondata = request.POST['oldresult']
				return HttpResponseRedirect('/result?file=app/static/jsons/'+jsondata)
			else: 
				form = FileChoosingform()
				return render(request, 'filechoosing.html', {'form' : form, 'form_results' : form_results})
	else:
		form = FileChoosingform()
		form_results = OldResultForm()
		form_results.fields['oldresult'].choices = CHOICES
		return render(request, 'filechoosing.html', {'form' : form, 'form_results' : form_results})


def datachoosing(request):
	if 'column' in request.session:
		CHOICES = buildtuple(request.session['column'])
	else:
		return HttpResponseRedirect('/')
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
			jsondata = saveData(request.session['path'], valueK, valueN, fields, jsonres)
			return HttpResponseRedirect('/result?file='+jsondata)
		else:
			return render(request, 'datachoosing.html', {'form' : form})
	else:
		form = DataChoosingform()
		form.fields['champs'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CHOICES)
		return render(request, 'datachoosing.html', {'form' : form})

def handle_uploaded_file(file, name):
	path = 'app/static/documents/' + name
	if not os.path.isfile(path):
		destination = open(path, 'a+')
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

def saveData(file, K, N, fields, jsondata):
	strtime = time.strftime("%Y-%m-%d-%H-%M-%S")
	path = 'app/static/jsons/' + strtime + '.json'
	data = {}
	data['file']   = file
	data['K']      = K
	data['N']      = N
	data['fields'] = fields
	data['json']   = jsondata
	with open(path, 'w+') as outfile:
		json.dump(data, outfile)
	return path

def getallsavedJson():
	res = [('None', '--------')]
	pathdir = 'app/static/jsons/'
	for f in listdir(pathdir):
		if isfile(join(pathdir,f)):
			res.append((str(f),str(f)))
	return res