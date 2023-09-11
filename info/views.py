from django.shortcuts import render, redirect
from .forms import SearchtoolForm
from django.http import HttpResponseRedirect
from tools.models import Toolsonwarehouse, Tools, Priem
from order.models import Order


def info(request):
    if request.GET.get('tool'):
        form = SearchtoolForm(request.GET)
        result = request.GET.get('tool')
        print(result)
        tools=Toolsonwarehouse.objects.filter(title__icontains  = result.upper()).all()
        toolsv=Tools.objects.filter(tool__title__icontains  = result.upper())
        priems = Priem.objects.filter(tool__title__icontains  = result.upper())
        orders = Order.objects.filter(tool__title__icontains  = result.upper())
        return render(request, 'info.html', {'tools':tools, 'toolsv':toolsv, 'priems':priems, 'orders':orders, 'form':form})
    form = SearchtoolForm()
    return render(request, 'info.html', { 'form':form})


