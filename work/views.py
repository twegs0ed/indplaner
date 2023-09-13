from django.shortcuts import render
from tools.models import Toolsonwarehouse
from .models import WorkForm, Work
from django.shortcuts import redirect


# Create your views here.
def add(request, id):
    if request.method == "POST":
        form = WorkForm(request.POST)
        if form.is_valid():
            work = form.save(commit=False)
            work.user = request.user
            work.save()
            return redirect('/work/work/'+str(work.pk)+'/change/')
    else:
        tool = Toolsonwarehouse.objects.get(pk=id)
        form=WorkForm(initial={'tool': tool, 'user':request.user})
        return render(request, 'work.html', { 'form':form})
def detail(request, pk):
    work=Work.objects.get(pk)
    return render(request, 'work.html', { 'work':work})