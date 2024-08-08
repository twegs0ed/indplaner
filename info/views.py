from django.shortcuts import render, redirect
from .forms import GanttForm, SearchtoolForm, GetFirms, GetFirmsforstock
from django.http import HttpResponseRedirect
from tools.models import Toolsonwarehouse, Tools, Priem
from zink.models import Toolsonwarehousezn, Toolszn, Priemzn
from order.models import Order, Firm
from work.models import Work
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from datetime import datetime, timedelta, date
from django.utils.dateformat import format
import pandas as pd
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from django.http import Http404
from django.http import JsonResponse
from django.views.generic import View
from django.urls import reverse


def info(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login')) # or http response
    if request.GET.get('tool'):
        form = SearchtoolForm(request.GET)
        result = request.GET.get('tool')
        tools=Toolsonwarehouse.objects.filter(title__icontains  = result.upper()).order_by('-id')
        toolsv=Tools.objects.filter(tool__title__icontains  = result.upper()).order_by('-id')
        priems = Priem.objects.filter(tool__title__icontains  = result.upper()).order_by('-id')
        orders = Order.objects.filter(tool__title__icontains  = result.upper(), firm__report = False)
        orders_similar = Order.objects.none()
        '''.order_by('-id')'''
        mezhop = Toolsonwarehousezn.objects.filter(tool__title__icontains  = result.upper()).order_by('-id')
        similar=[]
        for tool in tools:
            try:
                tool.count_mezhop+=Toolsonwarehousezn.objects.get(tool = tool).count
            except Toolsonwarehousezn.DoesNotExist:
                        pass
            try:
                tool.count_all+=Toolsonwarehouse.objects.get(title = tool.title).count
            except Toolsonwarehouse.DoesNotExist:
                        pass
            for t_c in tool.similar.all():
                if t_c != tool:
                    if t_c not in similar:
                        similar.append(t_c)
                    try:
                        tool.count_mezhop+=Toolsonwarehousezn.objects.get(tool = t_c).count
                    except Toolsonwarehousezn.DoesNotExist:
                        pass
                    try:
                        tool.count_all+=Toolsonwarehouse.objects.get(title = t_c.title).count
                    except Toolsonwarehouse.DoesNotExist:
                        pass
        '''for ord in orders: 
            logs = LogEntry.objects.filter(content_type__app_label='order', object_id = ord.id).order_by('-action_time').first()#or you can filter, etc.
            if logs: 
                ord.log=logs.action_time'''
        for sim in similar:
            orders_sim = Order.objects.filter(tool= sim, firm__report = False)
            '''.order_by('-id')'''
            orders_c = orders_similar.union(orders_sim)
            orders_similar=orders_c
        orders.order_by('-id')

        
                
        mezhopgetout = Toolszn.objects.filter(tool__tool__title__icontains  = result.upper()).order_by('-id')
        mezhoppriem = Priemzn.objects.filter(tool__title__icontains  = result.upper()).order_by('-id')


        

        works = Work.objects.filter(tool__title__icontains  = result.upper()).order_by('-id')
        vars = {
            'tools':tools, 
            'toolsv':toolsv, 
            'priems':priems, 
            'orders':orders, 
            'orders_similar':orders_similar, 
            'works':works, 
            'form':form, 
            'mezhop':mezhop,
            'mezhopgetout':mezhopgetout,
            'mezhoppriem':mezhoppriem
            }
        return render(request, 'info.html', vars)
    form = SearchtoolForm()
    return render(request, 'info.html', { 'form':form})


def gantt(request):
    if request.GET.get('tool'):
        t_title=request.GET.get('tool')
        #project=Firm.objects.filter(title__icontains  = request.GET.get('tool')).first()
        project=Firm.objects.get(pk = int(request.GET.get('tool')))
        t_title = project.title
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
    cncturn_fact = 0
    cncmill_fact = 0
    for p in projects:
        if p.count:
            cncturn_fact_c, cncmill_fact_c = p.tool.getcncnorms(p.count)
            cncturn_fact += cncturn_fact_c/60
            cncmill_fact += cncmill_fact_c/60
            mill+=(p.tool.norm_mill*p.count)+p.tool.norm_mill_p
            turn+=(p.tool.norm_turn*p.count)+p.tool.norm_turn_p
            millun+=(p.tool.norm_millun*p.count)+p.tool.norm_millun_p
            turnun+=(p.tool.norm_turnun*p.count)+p.tool.norm_turnun_p
            lentopil+=(p.tool.norm_lentopil*p.count)+p.tool.norm_lentopil_p
            plazma+=(p.tool.norm_plazma*p.count)+p.tool.norm_plazma_p
            electro+=(p.tool.norm_electro*p.count)+p.tool.norm_electro_p
            slesarn+=p.tool.norm_slesarn*p.count
            sverliln+=(p.tool.norm_sverliln*p.count)+p.tool.norm_sverliln_p
    koaf2smen=(3/2)*(3/2) #=24/16(из 24 часов только 16 рабочие) и из 30 дней только 20 рабочие
    koaf1smen=(3/1)*(3/2)
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

    cncturn_fact_d = cncturn_fact/int(turnscnc)*koaf2smen
    cncmill_fact_d = cncmill_fact/int(millscnc)*koaf2smen
  
    def status(x):
        if x=="OW": return "В запуске"
        if x=="OR": return "Запущено"
        if x=="PD": return "На стороне"
        if x=="CM": return "Изготовлено"
        pass
    projects_data=[]
    if cncturn_fact:
        projects_data.append({
            'Операция':'Токарная с ЧПУ фактическая',
            'Start': project.date,
            'Finish': project.date+timedelta(hours=cncturn_fact_d),
            'Общее время': str(cncturn_fact)+' час.'
        })
    if cncmill_fact:
        projects_data.append({
            'Операция':'Фрезерная с ЧПУ фактическая',
            'Start': project.date,
            'Finish': project.date+timedelta(hours=cncmill_fact_d),
            'Общее время': str(cncmill_fact)+' час.'
        })
    
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
    cncturn_fact = 0.0
    cncmill_fact = 0.0
    for p in projects:
       
        if p.count:
            cncturn_fact_c, cncmill_fact_c = p.tool.getcncnorms(p.count)
            cncturn_fact += cncturn_fact_c/60
            cncmill_fact += cncmill_fact_c/60

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
        'cncturn_fact': cncturn_fact,
        'cncmill_fact':cncmill_fact
        }
    

    projects_data = [
        {
            'Операция': "токарная с ЧПУ факт.",
            'Время, ч': cncturn_fact,
        }, 
        {
            'Операция': "Фрезерная с ЧПУ факт",
            'Время, ч': cncmill_fact,
        }, 
        
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


def report(request):
    if request.POST.get('firms'):
        form = GetFirms(request.POST)
        firms = request.POST.getlist('firms')
        firms = Firm.objects.filter(pk__in=firms).order_by('exp_date').all()

        datestart = request.POST.get('datestart')
        dateend = request.POST.get('dateend')
        
        priems = Priem.objects.filter(giveout_date__gte=datestart, giveout_date__lte=dateend)
        orders=get_result_for_period(firms, priems)
        
        count={}
        for firm in firms:
            orders_count=0
            percents=0
            for order in orders:
                if order.firm == firm:
                    orders_count+=1
                    percents+=order.percent

            count[firm]=round (percents/orders_count, 2)
            
                    


        


        vars = {
            'firms':firms,
            'form':form,
            'title':'Отчет за период',
            'orders':orders,
            'count':count
            }
        
        return render(request, 'report.html', vars)
    form = GetFirms()
    vars = {
            'form':form,
            'title':'Отчет за период'
            }
    
    return render(request, 'report.html', vars)


def get_result_for_period(firms, priems):
    orders = []
    for firm in firms:
        for order in Order.objects.filter(firm=firm).all():
            orders.append(order)
            pass
    for order in orders:
            order.count = order.count*order.firm.count
    priems=list(priems)
    priems_copy = priems.copy()
    tools={}

    for priem in priems_copy:
        
        if not priem.tool.title in tools:
            tools[priem.tool.title]=priem.count
        else:
            tools[priem.tool.title]+=priem.count
        pass

    
    for tool in list(tools):
        tool_c = Toolsonwarehouse.objects.get(title = tool)
        for tool_similar in tool_c.similar.all():
            if (tool_similar.title in tools) and (not tool_similar.title == tool):
                try:
                    #print(tool, tools[tool])
                    tools[tool]+=tools[tool_similar.title] 
                    #print(tool, tools[tool])
                except:
                    pass
                #del tools[tool_similar.title]
            pass
        pass

    for order in orders:
        for tool_similar in order.tool.similar.all():
            if (tool_similar.title in tools) and (not order.tool.title == tool_similar.title):
                order.tool = Toolsonwarehouse.objects.get(title = tool_similar.title)
                #print(tool_similar, ' - ', order.tool.title)
        pass

    for priem in list(tools):
        while tools[priem] > 0:
            for order in orders:
                
                if (order.tool.title == priem):
                    order.priem = tools[priem]
                    if order.count < tools[priem]:
                        order.percent = 100
                        tools[priem]-=order.count
                    elif order.count == tools[priem]:
                        order.percent = 100
                        tools[priem]=0
                        #del tools[priem]
                        #break
                    elif order.count > tools[priem]:
                        order.percent = round(tools[priem]/order.count*100, 2)
                        tools[priem]=0
                        #del tools[priem]
                        #break
            break
    '''for priem in priems.copy():
        while priem.count > 0:
            for order in orders:
                if order.tool == priem.tool:
                    if order.count < priem.count:
                        order.percent = 100
                        priem.count-=order.count
                    elif order.count == priem.count:
                        order.percent = 100
                        priem.count=0
                        priems.remove(priem)
                        break
                    elif order.count > priem.count:
                        order.percent = priem.count/order.count*100
                        priem.count=0
                        priems.remove(priem)
                        break
            
            break'''
        
    
    return orders

def stock(request):
    
    if request.POST:
        firms = Firm.objects.filter(report = True).all()
        orders = Order.objects.none()
        for firm in firms:
            firm.count = request.POST.get('firm%s' % firm.id)
            orders_c = Order.objects.filter(firm=firm).all()
            #for ord in orders_c:
               #ord.count = ord.count*firm.count
            orders = orders.union(orders_c)
        tools={}
        for order in orders:
            order.count = order.count * int(request.POST.get('firm%s' % order.firm.id))
        orders=list(orders)
        for order in orders:
            tool = order.tool
            for tool_c in tool.similar.all():
                for or_c in orders:
                    if (tool_c != order.tool) & (tool_c == or_c.tool):
                        order.count+=or_c.count
                        orders.remove(or_c)
                        #print(tool_c.title, order.firm)
        for order in orders:
            if order.tool.title in tools:
                tools[order.tool.title] = [tools[order.tool.title][0]+order.count, order.tool.count,0]
            else:
                tools[order.tool.title]=[order.count, order.tool.count,0]
            #tools[order.tool.title+order.firm.title]=[order.count, order.tool.count]
        for key, value in list(tools.items()):
            if value[0] < 1:
                del tools[key]
        for key, value in list(tools.items()):
            tool_c = Toolsonwarehouse.objects.filter(title = key).first()
            #value[2]=list(tool_c.similar.all())
            for t_c in tool_c.similar.all():
                if t_c.title not in key:
                    value[1]+=t_c.count
            tools[key]=value
        for key, value in list(tools.items()):
            tools[key][2]=tools[key][0]-tools[key][1]

        
        
        



        form = GetFirmsforstock(request.POST)

        vars = {
            'form':form,
            'orders':tools,
            'title':'Склад',
            }
        
        return render(request, 'stock.html', vars)
    form = GetFirmsforstock()
    vars = {
            'form':form,
            'title':'Склад'
            }
    
    return render(request, 'stock.html', vars)

    
    
        
    


