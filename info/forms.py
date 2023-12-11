from django import forms

class SearchtoolForm(forms.Form):
    tool = forms.CharField(label='Деталь', max_length=100)

class GanttForm(forms.Form):
    tool = forms.CharField(label='Изделие', max_length=100)
    turnscnc = forms.IntegerField(label='Токарных ЧПУ',  initial=1)
    millscnc = forms.IntegerField(label='Фрезерных ЧПУ',  initial=1)
    turnunscnc = forms.IntegerField(label='Токарных универс.',  initial=1)
    millunscnc = forms.IntegerField(label='Фрезерных универс.',  initial=1)