from django import forms
from order.models import Firm

class SearchtoolForm(forms.Form):
    tool = forms.CharField(label='Деталь', max_length=100, widget=forms.TextInput(attrs={'size':40}))
    #tool = forms.ModelChoiceField(queryset=Firm.objects.all(), widget=forms.Select())

class GanttForm(forms.Form):
    #tool = forms.CharField(label='Изделие', max_length=100)
    tool = forms.ModelChoiceField(queryset=Firm.objects.all().order_by('-id')    , widget=forms.Select())
    turnscnc = forms.IntegerField(label='Токарных ЧПУ',  initial=1)
    millscnc = forms.IntegerField(label='Фрезерных ЧПУ',  initial=1)
    turnunscnc = forms.IntegerField(label='Токарных универс.',  initial=1)
    millunscnc = forms.IntegerField(label='Фрезерных универс.',  initial=1)
class GetFirms(forms.Form):
    #tool = forms.CharField(label='Изделие', max_length=100)
    '''def __init__(self, queryset, *args, **kwargs):
        super(GetFirms, self).__init__(*args, **kwargs)
        self.fields['firms'] = forms.ModelMultipleChoiceField(queryset=Firm.objects.filter(report = True).all(),       widget=forms.CheckboxSelectMultiple())'''
    firms = forms.ModelMultipleChoiceField(
        widget = forms.CheckboxSelectMultiple(attrs={'checked':True}),
        queryset = Firm.objects.filter(report = True).all(),
        initial = 0,
        label = 'Изделия для расчета',
        required=True, 
        )
    datestart = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),label='Начало периода')
    dateend = forms.DateTimeField( widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),label='Конец периода')
    