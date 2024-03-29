from django.shortcuts import render, redirect
from .forms import GanttForm, SearchtoolForm
from django.http import HttpResponseRedirect
from tools.models import Toolsonwarehouse, Tools, Priem
from order.models import Order, Firm
from work.models import Work
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from datetime import datetime, timedelta
from django.utils.dateformat import format
import pandas as pd
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from django.http import Http404
from django.http import JsonResponse
from django.views.generic import View


def info(request):
    if request.GET.get('tool'):
        form = SearchtoolForm(request.GET)
        result = request.GET.get('tool')
        tools=Toolsonwarehouse.objects.filter(title__icontains  = result.upper()).order_by('-id')
        toolsv=Tools.objects.filter(tool__title__icontains  = result.upper()).order_by('-id')
        priems = Priem.objects.filter(tool__title__icontains  = result.upper()).order_by('-id')
        orders = Order.objects.filter(tool__title__icontains  = result.upper()).order_by('-id')

        for ord in orders:
            logs = LogEntry.objects.filter(content_type__app_label='order', object_id = ord.id).order_by('-action_time').first()#or you can filter, etc.
            if logs: 
                ord.log=logs.action_time

        works = Work.objects.filter(tool__title__icontains  = result.upper()).order_by('-id')
        return render(request, 'info.html', {'tools':tools, 'toolsv':toolsv, 'priems':priems, 'orders':orders, 'works':works, 'form':form})
    form = SearchtoolForm()
    return render(request, 'info.html', { 'form':form})


def gantt(request):
    if request.GET.get('tool'):
        t_title=request.GET.get('tool')
        #project=Firm.objects.filter(title__icontains  = request.GET.get('tool')).first()
        project=Firm.objects.get(pk = int(request.GET.get('tool')))
        form = GanttForm(initial=request.GET)
        projects = Order.objects.filter(firm= project).all()
        if not projects :
            raise Http404
    else:
        t_title="Не задано"
        order=Order
        order.count=0
        projects = [order]
        project=Firm
        project.date=datetime.now() 
        form = GanttForm(initial=request.GET)
    
    if request.GET.get('millscnc'):millscnc=request.GET.get('millscnc')
    else:millscnc=1
    if request.GET.get('turnscnc'):turnscnc=request.GET.get('turnscnc')
    else:turnscnc=1
    if request.GET.get('millunscnc'):millunscnc=request.GET.get('millunscnc')
    else:millunscnc=1
    if request.GET.get('turnunscnc'):turnunscnc=request.GET.get('turnunscnc')
    else:turnunscnc=1
    mill=0
    turn=0
    millun=0
    turnun=0
    lentopil=0
    plazma=0
    electro=0
    slesarn=0
    sverliln=0
    rastoch=0
    for p in projects:
        if p.count:
            mill+=(p.tool.norm_mill*p.count)+p.tool.norm_mill_p
            turn+=(p.tool.norm_turn*p.count)+p.tool.norm_turn_p
            millun+=(p.tool.norm_millun*p.count)+p.tool.norm_millun_p
            turnun+=(p.tool.norm_turnun*p.count)+p.tool.norm_turnun_p
            lentopil+=(p.tool.norm_lentopil*p.count)+p.tool.norm_lentopil_p
            plazma+=(p.tool.norm_plazma*p.count)+p.tool.norm_plazma_p
            electro+=(p.tool.norm_electro*p.count)+p.tool.norm_electro_p
            slesarn+=p.tool.norm_slesarn*p.count
            sverliln+=(p.tool.norm_sverliln*p.count)+p.tool.norm_sverliln_p
    koaf2smen=3/2 #=24/16(из 24 часов только 16 рабочие)
    koaf1smen=3/1
    mill_d=mill/int(millscnc)*koaf2smen
    turn_d=turn/int(turnscnc)*koaf2smen
    millun_d=mill/int(millunscnc)*koaf2smen
    turnun_d=turnun/int(turnunscnc)*koaf2smen
    lentopil_d=lentopil*koaf2smen
    plazma_d=plazma*koaf2smen
    electro_d=electro*koaf1smen
    slesarn_d=slesarn*koaf2smen
    sverliln_d=sverliln*koaf2smen
    rastoch_d=rastoch*koaf2smen

  
    def status(x):
        if x=="OW": return "В запуске"
        if x=="OR": return "Запущено"
        if x=="PD": return "На стороне"
        if x=="CM": return "Изготовлено"
        pass
    projects_data=[]
    print(mill)
    if mill:
        projects_data.append({
            'Операция':'Фрезерная с ЧПУ',
            'Start': project.date,
            'Finish': project.date+timedelta(hours=mill_d),
            'Общее время': str(mill)+' час.'
        })
    if turn:
        projects_data.append({
            'Операция':'Токарная с ЧПУ',
            'Start': project.date,
            'Finish': project.date+timedelta(hours=turn_d),
            'Общее время': str(turn)+' час.'
        })
    if millun:
        projects_data.append({
            'Операция':'Фрезерная универсальная',
            'Start': project.date,
            'Finish': project.date+timedelta(hours=millun_d),
            'Общее время': str(millun)+' час.'
        })
    if turnun:
        projects_data.append({
            'Операция':'Токарная Универсальная',
            'Start': project.date,
            'Finish': project.date+timedelta(hours=turnun_d),
            'Общее время': str(turnun)+' час.'
        })

    if lentopil:
        projects_data.append(
            {
                'Операция':'Ленточнопильная',
                'Start': project.date,
                'Finish': project.date+timedelta(hours=lentopil_d),
                'Общее время': str(lentopil)+' час.'
            } )
    if plazma:
        projects_data.append(
            {
                'Операция':'Плазменная резка',
                'Start': project.date,
                'Finish': project.date+timedelta(hours=plazma_d),
                'Общее время': str(plazma)+' час.'
            } )
    if electro:
        projects_data.append(
            {
                'Операция':'Электроэрозионная',
                'Start': project.date,
                'Finish': project.date+timedelta(hours=electro_d),
                'Общее время': str(electro)+' час.'
            } )
    if slesarn:
        projects_data.append(
            {
                'Операция':'Слесарная',
                'Start': project.date,
                'Finish': project.date+timedelta(hours=slesarn_d),
                'Общее время': str(slesarn)+' час.'
            } )
    if sverliln:
        projects_data.append(
            {
                'Операция':'Сверлильная',
                'Start': project.date,
                'Finish': project.date+timedelta(hours=sverliln_d),
                'Общее время': str(sverliln)+' час.'
            } )
    if rastoch:
        projects_data.append(
            {
                'Операция':'Расточная',
                'Start': project.date,
                'Finish': project.date+timedelta(hours=rastoch_d),
                'Общее время': str(rastoch)+' час.'
            } )
    if not projects_data:
        projects_data.append(
            {
                'Операция':'нет',
                'Start': datetime.now(),
                'Finish': datetime.now(),
                'Общее время': '0 час.'
            } )
    

    df = pd.DataFrame(projects_data)
    
    fig = px.timeline(
        df, x_start="Start", x_end="Finish", y="Операция", color="Операция",text="Общее время", title="Нормы по операциям",
                 hover_data=['Операция', 'Start', 'Finish', 'Общее время']
    )
    
    fig.update_yaxes(autorange="reversed")
    gantt_plot = plot(fig, output_type="div")


    lentopil=0.0
    plazma=0.0
    turn=0.0
    mill=0.0
    turnun=0.0
    millun=0.0
    electro=0.0
    slesarn=0.0
    sverliln=0.0
    rastoch=0.0
    for p in projects:
       
        if p.count:
            lentopil+=(p.tool.norm_lentopil*p.count)
            lentopil+=p.tool.norm_lentopil_p

            plazma+=p.tool.norm_plazma*p.count
            plazma+=p.tool.norm_plazma_p

            turn+=p.tool.norm_turn*p.count
            turn+=p.tool.norm_turn_p

            mill+=p.tool.norm_mill*p.count
            mill+=p.tool.norm_mill_p

            turnun+=p.tool.norm_turnun*p.count
            turnun+=p.tool.norm_turnun_p

            millun+=p.tool.norm_millun*p.count
            millun+=p.tool.norm_millun_p

            electro+=p.tool.norm_electro*p.count
            electro+=p.tool.norm_electro_p

            slesarn+=p.tool.norm_slesarn*p.count

            sverliln+=p.tool.norm_sverliln*p.count
            sverliln+=p.tool.norm_sverliln_p

            rastoch+=p.tool.norm_rastoch*p.count
            rastoch+=p.tool.norm_rastoch_p
    norms={
        'lentopil':lentopil,
        'plazma':plazma,
        'turn':turn,
        'mill':mill,
        'turnun':turnun,
        'millun':millun,
        'electro':electro,
        'slesarn':slesarn,
        'sverliln':sverliln,
        'rastoch':rastoch,
        }
    

    projects_data = [
        
        {
            'Операция': "Ленточнопильная",
            'Время, ч': lentopil,
        }, 
        {
            'Операция': "Плазма",
            'Время, ч': plazma,
        }, 
        {
            'Операция': "Токарная ЧПУ",
            'Время, ч': turn,
        },
        {
            'Операция': "Фрезерная ЧПУ",
            'Время, ч': mill,
        }, 
        {
            'Операция': "Токарная универс.",
            'Время, ч': turnun,
        },
        {
            'Операция': "Фрезерная универс.",
            'Время, ч': millun,
        }, 
        {
            'Операция': "Электроэрозионная",
            'Время, ч': electro,
        }, 
        {
            'Операция': "Слесарная",
            'Время, ч': slesarn,
        }, 
        {
            'Операция': "Сверлильная",
            'Время, ч': sverliln,
        }, 
        {
            'Операция': "Расточная",
            'Время, ч': rastoch,
        }, 
    ]
    dfh = pd.DataFrame(projects_data)

    hist = px.histogram(dfh, x="Операция",y="Время, ч", color="Операция", title='Трудозатраты по операциям', text_auto=True )
    hist_plot = plot(hist, output_type="div")

    context = {
        'plot_div': gantt_plot,
        'form':form,
        'hist_div': hist_plot,
        'norms':norms,
        't_title':t_title,
        'project':project
        }
    return render(request, 'gantt.html', context)




    
    
        
    


