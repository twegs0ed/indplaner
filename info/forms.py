from django import forms

class SearchtoolForm(forms.Form):
    tool = forms.CharField(label='Деталь', max_length=100)