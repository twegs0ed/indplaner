from django.shortcuts import render, redirect
from .forms import SearchtoolForm
from django.http import HttpResponseRedirect
from tools.models import Toolsonwarehouse, Tools, Priem
from order.models import Order
from work.models import Work
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION


def info(request):
    if request.GET.get('tool'):
        form = SearchtoolForm(request.GET)
        result = request.GET.get('tool')
        tools=Toolsonwarehouse.objects.filter(title__icontains  = result.upper()).all()
        toolsv=Tools.objects.filter(tool__title__icontains  = result.upper())
        priems = Priem.objects.filter(tool__title__icontains  = result.upper())
        orders = Order.objects.filter(tool__title__icontains  = result.upper())
        works = Work.objects.filter(tool__title__icontains  = result.upper())
        return render(request, 'info.html', {'tools':tools, 'toolsv':toolsv, 'priems':priems, 'orders':orders, 'works':works, 'form':form})
    form = SearchtoolForm()
    return render(request, 'info.html', { 'form':form})


