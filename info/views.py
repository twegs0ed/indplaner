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


def info(request):
    if request.GET.get('tool'):
        form = GanttForm(request.GET)
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
        t_title=request.GET.get('tool')
        project=Firm.objects.filter(title__icontains  = request.GET.get('tool')).first()
        #print(project[0]+'!!!!!!!!')
        form = GanttForm(initial=request.GET)
        projects = Order.objects.filter(firm__title__icontains  = request.GET.get('tool')).all()
        if not projects :
            raise Http404
    else:
        t_title="Не задано"
        projects = Order.objects.filter(firm__title__icontains  = '').order_by('exp_date').all()   
    
    if request.GET.get('millscnc'):millscnc=request.GET.get('millscnc')
    else:millscnc=1
    if request.GET.get('turnscnc'):turnscnc=request.GET.get('turnscnc')
    else:turnscnc=1
    mill=0
    turn=0
    for p in projects:
        mill+=(p.tool.norm_mill*p.count)+p.tool.norm_mill_p
        turn+=(p.tool.norm_turn*p.count)+p.tool.norm_turn_p
    mill_d=mill/8/2/int(millscnc)*30/20
    turn_d=turn/8/2/int(turnscnc)*30/20

    
    def status(x):
        if x=="OW": return "В запуске"
        if x=="OR": return "Запущено"
        if x=="PD": return "На стороне"
        if x=="CM": return "Изготовлено"
        pass
    projects_data=[
        {
            'Операция':'Фрезерная с ЧПУ',
            'Start': project.date,
            'Finish': project.date+timedelta(days=mill_d),
            'Общее время': str(mill/8/2/21)+' мес.'
        } ,
        {
            'Операция':'Токарная с ЧПУ',
            'Start': project.date,
            'Finish': project.date+timedelta(days=turn_d),
            'Общее время': str(turn/8/2/21)+' мес.'
        } 
    ]
    

    '''projects_data = [
        {
            'Деталь': x.tool.title,
            'Start': datetime.date(x.order_date_worker),
            'Finish': x.exp_date,
            'Статус': status(x.status)
        } for x in projects
    ]'''
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
        '''lentopil+=(p.tool.norm_lentopil*p.count)
        if p.count>0:lentopil+=p.tool.norm_lentopil_p/p.count

        plazma+=p.tool.norm_plazma*p.count
        if p.tool.count>0:plazma+=p.tool.norm_plazma_p/p.tool.count

        turn+=p.tool.norm_turn*p.count
        if p.tool.count>0:turn+=p.tool.norm_turn_p/p.tool.count

        mill+=p.tool.norm_mill*p.count
        if p.tool.count>0:mill+=p.tool.norm_mill_p/p.tool.count

        turnun+=p.tool.norm_turnun*p.count
        if p.tool.count>0:turnun+=p.tool.norm_turnun_p/p.tool.count

        millun+=p.tool.norm_millun*p.count
        if p.tool.count>0:millun+=p.tool.norm_millun_p/p.tool.count

        electro+=p.tool.norm_electro*p.count
        if p.tool.count>0:electro+=p.tool.norm_electro_p/p.tool.count

        slesarn+=p.tool.norm_slesarn*p.count

        sverliln+=p.tool.norm_sverliln*p.count
        if p.tool.count>0:sverliln+=p.tool.norm_sverliln_p/p.tool.count

        rastoch+=p.tool.norm_rastoch*p.count
        if p.tool.count>0:rastoch+=p.tool.norm_rastoch_p/p.tool.count'''
        lentopil+=(p.tool.norm_lentopil*p.count)
        if p.count>0:lentopil+=p.tool.norm_lentopil_p/p.count

        plazma+=p.tool.norm_plazma*p.count
        if p.tool.count>0:plazma+=p.tool.norm_plazma_p/p.tool.count

        turn+=p.tool.norm_turn*p.count
        if p.tool.count>0:turn+=p.tool.norm_turn_p/p.tool.count

        mill+=p.tool.norm_mill*p.count
        if p.tool.count>0:mill+=p.tool.norm_mill_p/p.tool.count

        turnun+=p.tool.norm_turnun*p.count
        if p.tool.count>0:turnun+=p.tool.norm_turnun_p/p.tool.count

        millun+=p.tool.norm_millun*p.count
        if p.tool.count>0:millun+=p.tool.norm_millun_p/p.tool.count

        electro+=p.tool.norm_electro*p.count
        if p.tool.count>0:electro+=p.tool.norm_electro_p/p.tool.count

        slesarn+=p.tool.norm_slesarn*p.count

        sverliln+=p.tool.norm_sverliln*p.count
        if p.tool.count>0:sverliln+=p.tool.norm_sverliln_p/p.tool.count

        rastoch+=p.tool.norm_rastoch*p.count
        if p.tool.count>0:rastoch+=p.tool.norm_rastoch_p/p.tool.count
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

    hist = px.histogram(dfh, x="Операция",y="Время, ч", color="Время, ч", title='Трудозатраты по операциям', text_auto=True )
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
    
    
        
    


