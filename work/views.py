from django.shortcuts import render
from tools.models import Toolsonwarehouse
from .models import WorkForm, Work
from django.shortcuts import redirect
from django.http import Http404


# Create your views here.
def add(request, id):
    print(request.get_host())
    if 'localhost' in request.get_host() or '1779247-cl68349.twc1.net' in request.get_host():
        return redirect('http://cptpsk.ru/work/work/add/'+str(id))
    try:
        tool = Toolsonwarehouse.objects.get(pk=id)
    except Toolsonwarehouse.DoesNotExist:
        raise Http404
    form_class = WorkForm
    form = form_class(request.POST or None)
    if request.method == "POST":
        form = WorkForm(request.POST)
        work = form.save(commit=False)
        work.save()
        return render(request, 'success.html', { 'form':form, 'tool' : tool.title})
    else:
        form=WorkForm(initial={'tool': tool, 'user':request.user})
        if request.user.groups.filter(name='master').exists():
            return redirect('/work/work/add/')
        if request.user.groups.filter(name='worker').exists():
            form.fields['user'].widget.attrs['readonly'] = True 
            form.fields['user'].widget.attrs['hidden'] = True 
            form.fields['tool'].widget.attrs['readonly'] = True 
            form.fields['tool'].widget.attrs['hidden'] = True 
            
        return render(request, 'work.html', { 'form':form, 'tool' : tool.title, 'user' : request.user})
def detail(request, pk):
    work=Work.objects.get(pk)
    return render(request, 'work.html', { 'work':work})