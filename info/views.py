from django.shortcuts import render, redirect
from .forms import SearchtoolForm
from django.http import HttpResponseRedirect
from tools.models import Toolsonwarehouse, Tools, Priem
from order.models import Order
from work.models import Work
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from datetime import datetime 
from django.utils.dateformat import format


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


def gantt(request):
    if request.GET.get('tool'):
        form = SearchtoolForm(request.GET)
        projects = Order.objects.filter(firm__title__icontains  = request.GET.get('tool')).all()
    else:
        projects = Order.objects.filter(firm__title__icontains  = '').order_by('exp_date').all()
    form = SearchtoolForm()
    
    

    
    data = [{
		'id': "1",
		'name': request.GET.get('tool'),
        
		'actualStart':int(round(projects[0].order_date_worker.timestamp() * 1000)),
		'actualEnd': int(round(datetime.timestamp(datetime.combine(projects[len(projects)-1].exp_date, datetime.min.time())))*1000)  ,
		'children': [
			

		]
	}]
    prew_id=0
    for p in projects:
        if p.exp_date:
            d=int(round(datetime.timestamp(datetime.combine(p.exp_date, datetime.min.time())))*1000) 
        else: d=1700164761000
        prc={
				'id': p.id,
				'name': p.tool.title,
				'actualStart':int(round(p.order_date_worker.timestamp() * 1000)),
                
		        'actualEnd': d,
				'connectTo': prew_id,
				'connectorType': "finish-start",
				'progressValue': "75%"
			}
        prew_id=p.id
        data[0]['children'].append(prc)
    
    
        
    return render(request, 'gantt.html', { 'data':data, 'form':form})


