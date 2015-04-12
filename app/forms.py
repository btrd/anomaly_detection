#-*- coding: utf-8 -*-
from django import forms

class FileChoosingform(forms.Form):
	filepath = forms.FileField(label ="Fichier csv")
	entete = forms.BooleanField(label = "nom dans l'entête ?", required=False, initial=True)
	filenamepath = forms.FileField(label ="Fichier des noms", required=False)

class DataChoosingform(forms.Form):
	CHOICES = (("0", "column0"),("1", "column1"),("2", "column2"),("3", "column3"),)
	valueK = forms.DecimalField(min_value = 0, label = "Valeur de K", help_text='valeur supérieur à 0')
	valueN = forms.DecimalField(min_value = 0, max_value = 100, label = "Valeur de N", help_text='valeur entre 0 et 100')
	champs = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CHOICES)