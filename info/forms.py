from django import forms
from order.models import Firm

class SearchtoolForm(forms.Form):
    tool = forms.CharField(label='Деталь', max_length=100)
    #tool = forms.ModelChoiceField(queryset=Firm.objects.all(), widget=forms.Select())

class GanttForm(forms.Form):
    #tool = forms.CharField(label='Изделие', max_length=100)
    tool = forms.ModelChoiceField(queryset=Firm.objects.all().order_by('-id')    , widget=forms.Select())
    turnscnc = forms.IntegerField(label='Токарных ЧПУ',  initial=1)
    millscnc = forms.IntegerField(label='Фрезерных ЧПУ',  initial=1)
    turnunscnc = forms.IntegerField(label='Токарных универс.',  initial=1)
    millunscnc = forms.IntegerField(label='Фрезерных универс.',  initial=1)