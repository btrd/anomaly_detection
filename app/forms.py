#-*- coding: utf-8 -*-
from django import forms


class FileChoosingform(forms.Form):
	csvfile = forms.FileField(label ="csv file")
	entete = forms.BooleanField(label = "name ahead ?", required=False, initial=False)

class DataChoosingform(forms.Form):
	index  = forms.IntegerField(min_value = 0, label="Classes index",help_text = "Index of the column containing the classes names")
	valueK = forms.DecimalField(min_value = 0, label = "K value", help_text='value greater than 0')
	valueN = forms.DecimalField(min_value = 0, max_value = 100, label = "N value", help_text='value between 0 and 100')
	champs = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

class OldResultForm(forms.Form):
	oldresult = forms.ChoiceField(label ="Old Result")