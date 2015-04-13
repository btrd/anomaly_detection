#-*- coding: utf-8 -*-
from django import forms


class FileChoosingform(forms.Form):
	csvfile = forms.FileField(label ="Fichier csv")
	entete = forms.BooleanField(label = "nom dans l'entête ?", required=False, initial=False)
	#namefile = forms.FileField(label ="Fichier des noms", required=False)

class DataChoosingform(forms.Form):
	valueK = forms.DecimalField(min_value = 0, label = "Valeur de K", help_text='valeur supérieur à 0')
	valueN = forms.DecimalField(min_value = 0, max_value = 100, label = "Valeur de N", help_text='valeur entre 0 et 100')
	champs = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)#, choices=CHOICES)