from django.shortcuts import render
from tools.models import Toolsonwarehouse
from .models import WorkForm, Work
from django.shortcuts import redirect


# Create your views here.
def add(request, id):
    tool = Toolsonwarehouse.objects.get(pk=id)
    form_class = WorkForm
    form = form_class(request.POST or None)
    if request.method == "POST":
        form = WorkForm(request.POST)
        work = form.save(commit=False)
        work.save()
        return render(request, 'success.html', { 'form':form, 'tool' : tool.title})
    else:
        form=WorkForm(initial={'tool': tool, 'user':request.user})
        form.fields['user'].widget.attrs['readonly'] = True 
        #form.fields['user'].widget.attrs['disabled'] = True 
        form.fields['user'].widget.attrs['hidden'] = True 
        form.fields['tool'].widget.attrs['readonly'] = True 
        #form.fields['tool'].widget.attrs['disabled'] = True 
        form.fields['tool'].widget.attrs['hidden'] = True 
        return render(request, 'work.html', { 'form':form, 'tool' : tool.title, 'user' : request.user})
def detail(request, pk):
    work=Work.objects.get(pk)
    return render(request, 'work.html', { 'work':work})