from django.contrib import admin
from .models import Order, Firm, Orderformed, Assem
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from import_export import resources
from tools.models import Toolsonwarehouse, Tools, Norms
from django.contrib.admin.models import LogEntry
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from rangefilter.filters import DateRangeFilter
from django.forms import TextInput, Textarea
from django.db import models
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.contrib.admin.models import LogEntry
from datetime import datetime
from work.models import Work
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.db.models import Q




def unfinished(modeladmin, request, queryset):

    orders=[]
    
    for firm_c in queryset:
        for ords_c in Order.objects.filter(firm=firm_c).filter(Q(status=Order.ORDERED_BY_WORKER) | Q(status=Order.ORDERED)).all():
            orders.append(ords_c)
        
    return render(request, 'unfinished.html', {'orders': orders, 'title':u'Незавершенное производство'})
unfinished.short_description = "Незавершенка"#заказано
#Меняем статус заказа на  заказано
def make_ordered(modeladmin, request, queryset):
    
    queryset.update(status= Order.ORDERED)
make_ordered.short_description = "Статус запущено"#заказано

#Меняем статус заказа на оплачен
def make_payed(modeladmin, request, queryset):
    queryset.update(status= Order.PAYED)
make_payed.short_description = "Статус отдано на сторону"#оплачено

#Меняем статус заказа на "получен"
def make_com(modeladmin, request, queryset):
    queryset.update(status= Order.COM)
make_com.short_description = "Статус изготовлено"#получено

#Меняем статус заказа на закзаан рабочим
def make_ordered_by_worker(modeladmin, request, queryset):
    queryset.update(status= Order.ORDERED_BY_WORKER)
make_ordered_by_worker.short_description = "Статус в запуске"#заяввка

def count_minus(queryset):
    orderformed = Orderformed()
    orderformed.status = Order.ORDERED
    orderformed.save()
    for e in queryset.all():
        orderformed.tools.add(e)

    #Уменьшаем количество на складе, так как статус было получено
    if queryset.values()[0]['status'] == Order().COM:#если предыдущий статус был "получено"
        tool = Toolsonwarehouse.objects.get(id=queryset.values()[0]['tool_id'])
        tool.count = int(tool.count) - int(queryset.values()[0]['count'])#то количество инструмента на складе уменьшаем
        tool.save()

def count_plus(queryset):
    #Увеличиваем количество, так как статус было не получено
    if queryset.values()[0]['status'] != Order().COM:#если предыдущий статус был не "получено"
        tool = Toolsonwarehouse.objects.get(id=queryset.values()[0]['tool_id'])
        tool.count = int(tool.count) + int(queryset.values()[0]['count'])#то количество инструмента на складе уменьшаем
        tool.save()




def status_colored(obj):
    return mark_safe('<b style="background:{};">{}</b>'.format(obj.color,'______')+'<br><b style="background:{};">{}</b>'.format(obj.color2, '______'))
status_colored.allow_tags = True
status_colored.short_description = "Цвет"





  
def status_order_colored(obj):
    if obj.firm != None:
        return mark_safe('<b style="background:{};">{}</b>'.format(obj.firm.color,'______')+'<br><b style="background:{};">{}</b>'.format(obj.firm.color2, '______'))
    return mark_safe('<b style="background:{};">{}</b>'.format('white','______')+'<br><b style="background:{};">{}</b>'.format('white', '______'))
status_order_colored.allow_tags = True
status_order_colored.short_description = "Цвет"
def tool_cover(obj):
    if obj.tool:
        if obj.tool.cover == False:
            cv='Нет'
            return mark_safe('<b style="background:#FF7878;">{}</b>'.format(cv))
        elif obj.tool.cover == True:
            cv='Да'
            return mark_safe('<b style="background:#0EFF23;">{}</b>'.format(cv))
    return 0
tool_cover.allow_tags = True
tool_cover.short_description = "покр."




class ForeignKeyWidgetWithCreation (ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        try:
            return super(ForeignKeyWidgetWithCreation, self).clean(value, row, *args, **kwargs)
        except:
            return self.model.objects.create(**{self.field: value})
#получить нормы ПЗ для детали токарной с ЧПУ


class OrderResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        Firm.objects.get_or_create(
            title=row.get('firm')
        )
        Toolsonwarehouse.objects.get_or_create(
            title=row.get('tool')
        )
    tool = Field(column_name='tool',attribute='tool',widget=ForeignKeyWidget(model=Toolsonwarehouse, field='title'))
    count_avail = Field()
    count_avail_all = Field()
    place = Field()
    firm = Field(column_name='firm',attribute='firm',widget=ForeignKeyWidget(model=Firm, field='title'))
    


    tool_material_n = Field()
    tool_stocksizes= Field()
    getout = Field()
    cover = Field()
    firms = Field()

    norm_turn_cnc = Field()
    norm_mill_cnc = Field()
    norm_turntpz_cnc = Field()
    norm_milltpz_cnc = Field()
    
    
    
       
    
    class Meta:
        model = Order
        fields = ('tool', 'count','exp_date', 'firm', 'status', 'folder')
        
        export_order = ('tool', 'count', 'exp_date','firm')
        import_id_fields = ('tool','firm')


    def dehydrate_count_avail(self, order): 
        if order.tool: return order.tool.count
    def dehydrate_count_avail_all(self, order): 
        if order.tool:
            count = order.tool.count
            for t_c in order.tool.similar.all():
                if order.tool.title != t_c.title:count+=t_c.count
            return count
        return 0
    def dehydrate_place(self, order): 
        if order.tool: return order.tool.workplace
    def dehydrate_tool_material_n(self, order): 
        if order.tool: return order.tool.material_n
    def dehydrate_tool_stocksizes(self, order): 
        if order.tool: return order.tool.stock_sizes


    def dehydrate_norm_lentopil_p(self, order): 
        if order.tool: return order.tool.norm_lentopil_p
    def dehydrate_status(self, order):  
        if order.status == 'OW' : return 'В запуске'
        if order.status == 'OR' : return 'Запущено'
        if order.status == 'PD' : return 'На стороне'
        if order.status == 'CM' : return 'Изготовлено'
    
    
    def dehydrate_norm_turn_cnc(self, order): 
        
        try:
            norms = Norms.objects.get(tool=order.tool)
        except Norms.DoesNotExist:
            return 0
        
        t=int(norms.cncturn1 or 0)+int(norms.cncturn2 or 0)+int(norms.cncturn3 or 0)+int(norms.cncturn4 or 0)+int(norms.cncturn5 or 0)+int(norms.cncturn6 or 0)+int(norms.cncturn7 or 0)
        t=t*order.count
        return t
    def dehydrate_norm_mill_cnc(self, order): 
        
        try:
            norms = Norms.objects.get(tool=order.tool)
        except Norms.DoesNotExist:
            return 0
        
        t=int(norms.cncmill1 or 0)+int(norms.cncmill2 or 0)+int(norms.cncmill3 or 0)+int(norms.cncmill4 or 0)+int(norms.cncmill5 or 0)+int(norms.cncmill6 or 0)+int(norms.cncmill7 or 0)
        t=t*order.count
        t=t
        return t
    def dehydrate_norm_turntpz_cnc(self, order): 
        t = 0
        try:
            norms = Norms.objects.get(tool=order.tool)
        except Norms.DoesNotExist:
            return 0
        
        if norms.cncturn1:t+=1
        if norms.cncturn2:t+=1
        if norms.cncturn3:t+=1
        if norms.cncturn4:t+=1
        if norms.cncturn5:t+=1
        if norms.cncturn6:t+=1
        if norms.cncturn7:t+=1
        return t*25
    def dehydrate_norm_milltpz_cnc(self, order): 
        t = 0
        try:
            norms = Norms.objects.get(tool=order.tool)
        except Norms.DoesNotExist:
            return 0
        
        if norms.cncmill1:t+=1
        if norms.cncmill2:t+=1
        if norms.cncmill3:t+=1
        if norms.cncmill4:t+=1
        if norms.cncmill5:t+=1
        if norms.cncmill6:t+=1
        if norms.cncmill7:t+=1
        return t*25
        

            
        
 

    def dehydrate_getout(self, obj):  
        w=Tools.objects.filter(tool=obj.tool).order_by('-giveout_date').all()[:3]
        t=""
        if w:
            for l in w: 
                name=l.worker.bio+' '
                
                t+=name
                t+=datetime.strftime(l.giveout_date, '%d.%m.%Y')
                t+=' - '+str(l.count)+' шт. '
            t+=' место: '+str(obj.tool.workplace)+' - '+str(obj.tool.count)+' шт.'
        return format_html(t)
    def dehydrate_cover(self, order):  
        if order.tool: 
            if order.tool.cover: return 1
            else: return 0

    def dehydrate_firms(self, obj):
        orders=Order.objects.filter(tool=obj.tool).order_by('-order_date_worker').all()[:10]
        t=""
        for l in orders: 
            t+=l.firm.title+';' if l.firm else 'нет'
            
        return t

            



class OrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
       
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':15})},
    }
    resource_class = OrderResource
    list_display = ('tool','count', 'c_count', 'c_count_all', 'status', 'firm', status_order_colored, 'exp_date','text', 'printmk', tool_cover, 'log', 'work', 'getout', 'firms', 'folder1')
    list_filter = (('exp_date', DateRangeFilter),'status', )
    search_fields = ['tool__title', 'firm__title']
    autocomplete_fields = [ 'tool', 'firm']
    actions = [make_ordered, make_payed, make_com, make_ordered_by_worker]
    list_editable = ['firm', 'count','exp_date', 'text', 'status']
    ordering = ['-order_date_worker', 'exp_date','-status']

#вывод выдачи в admin/order
    def getout(self, obj):
        w=Tools.objects.filter(tool=obj.tool).order_by('-giveout_date').all()[:3]
        t=""
        for l in w: 
            name=l.worker.bio+' '
            
            t+='<a href="/tools/toolsonwarehouse/?q='+l.tool.title+'"><p style="background-color:;"><font color=""><b>'+name+'</b></font> '
            t+=datetime.strftime(l.giveout_date, '%d.%m.%Y')
            t+=' - '+str(l.count)+' шт. '
            t+='<br></p></a>'
        t+='</br>место: '+str(obj.tool.workplace)+' - '+str(obj.tool.count)+' шт.'
        return format_html(t)
    getout.short_description = "Выдача"
#вывод фирм в которые еще входит деталь
    def firms(self, obj):
        orders=Order.objects.filter(tool=obj.tool).order_by('-order_date_worker').all()[:10]
        t=""
        for l in orders: 
            t+=l.firm.title+'</br>' if l.firm else 'нет'
            
        return format_html(t)
    firms.short_description = "др.изд."
#печать маршрутки
    def printmk(self, obj):
        url = '/order/printmk'
        url = url + '/'+str(obj.id)
        return format_html('<a href="{}" class="button">&#128438;</a>', url)
    printmk.short_description = "МК"
#путь до чертежа детали на сервере
    def folder1(self, obj):
        if obj.folder:
            url=obj.folder
            url= url.replace('"', '')
            url= url.replace('\\', '\\\\')
            return format_html('<button type="button" onclick="copyToClipboard(\'{}\')">  &dArr;  </button>', url,)
        return 'Нет'
    folder1.short_description = "pdf"
    

#вывод норм в админ order
    def norms(self, obj):
        t=''
        norms_cnc_turn, norms_cnc_mill = obj.tool.getcncnorms(obj.count)

        
        if obj.tool:
            #t=str(obj.tool.title)+'</br>'

            t+='ток.чпу.:'+str(norms_cnc_turn)+'</br>'
            t+='фрез.чпу:'+str(norms_cnc_mill)+'</br>'

            '''
            t+='Ленточнопильная:'+str(obj.tool.norm_lentopil)+'</br>'
            t+='Плазма:'+str(obj.tool.norm_plazma)+'</br>'
            t+='ток.чпу.:'+str(obj.tool.norm_turn)+'</br>'
            t+='фрез.чпу:'+str(obj.tool.norm_mill)+'</br>'
            t+='ток.унив.:'+str(obj.tool.norm_turnun)+'</br>'
            t+='фрез.унив.:'+str(obj.tool.norm_millun)+'</br>'
            t+='сверл.:'+str(obj.tool.norm_sverliln)+'</br>'
            t+='слесарн.:'+str(obj.tool.norm_slesarn)+'</br>'
            t+='электроэроз.:'+str(obj.tool.norm_electro)+'</br>'
            t+='электроэроз.:'+str(obj.tool.norm_electro)+'</br>'
            t+='расточ.:'+str(obj.tool.norm_rastoch)+'</br>'
            t+='расточ.:'+str(obj.tool.norm_rastoch)+'</br>'
        '''
            
        
        
        return format_html(t)
    norms.short_description = "Нормы" 
    def log(self, obj):
        logs = LogEntry.objects.filter(content_type__app_label='order', object_id = obj.id).order_by('action_time').all()#or you can filter, etc.
        t=""
        for l in logs: 
            try:
                name=l.user.last_name+' '+l.user.first_name[0]
            except IndexError:
                name=l.user.last_name+' '+l.user.first_name
            t+='<p style="background-color:;"><font color=""><b>'+name+'</b></font>'
            t+=" "
            if l.action_flag==1:t+="добавил "
            if l.action_flag==2:t+="изменил "
            if l.action_flag==3:t+="удалил "
            t+=datetime.strftime(l.action_time, '%d.%m.%Y')
            t+='<br></p>'

        return format_html(t)
    log.short_description = "История"
    def work(self, obj):
        w=Work.objects.filter(tool=obj.tool).order_by('-date', '-time').all()[:1]
        t=""
        for l in w: 
            try:
                name=l.user.last_name+' '+l.user.first_name[0]
            except IndexError:
                name=l.user.last_name+' '+l.user.first_name
            t+='<a href="/work/work/?q='+l.tool.title+'"><p style="background-color:;"><font color=""><b>'+name+'</b></font> '
            t+=datetime.strftime(l.date, '%d.%m.%Y')
            t+=' - '+str(l.count)+' шт. '
            t+=str(l.user.stanprofile.operation)
            t+='('
            for mach in l.user.stanprofile.machines.all() :
                t+=str(mach)+' / '
            t+=')'
            t+='<br></p></a>'

        return format_html(t)
    work.short_description = "Изгот-е"
#вывести сколько всего деталей с учетом похожих с другим шифром
    def c_count_all(self, obj):
        if obj.tool:
            title=obj.tool.title
            count=obj.tool.count
            for t_c in obj.tool.similar.all():
                if title != t_c.title:count+=t_c.count
            
        else: 
            title='1'
            count='0'
        t=str(count)
        return format_html(t)
    c_count_all.short_description = "На скл. все шифры"


#вывести в admin/order сколько на складе таких деталей
    def c_count(self, obj):
        if obj.tool:
            title=obj.tool.title
            count=obj.tool.count
        else: 
            title='1'
            count='0'
        t=' <a href = "/tools/toolsonwarehouse/?q='+str(title)+'">'+str(count)+'</a> '
        return format_html(t)
    c_count.short_description = "На скл."
    
    
    class Media:
        css = {
            'all': (
                'css/fancy.css',
            )
        }
        js = [
            'js/guarded_admin.js',
              'js/list_filter_collapse.js'
              ]
    
class FirmResource(resources.ModelResource):
    
    ready = Field()
    def dehydrate_ready(self, obj):  
        orders = Order.objects.filter(firm=obj).all().count()
        orders_ready = Order.objects.filter(firm=obj).filter(status='CM').all().count()
        if orders:
            result =  (orders_ready/orders)*100
            result = str(round(result,1))+'%'
        else: result='нет дет.'
        return result

   

    class Meta:
        model = Firm
        
        #fields = ('tool__title', 'count','worker__bio', 'giveout_date')
        #export_order = ('tool__title', 'worker__bio', 'count')

class ForeignKeyWidgetWithCreation (ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        try:
            return super(ForeignKeyWidgetWithCreation, self).clean(value, row, *args, **kwargs)
        except:
            return self.model.objects.create(**{self.field: value})

def svod_action(modeladmin, request, queryset):
    orders=[]
    
    for firm_c in queryset:
        for ords_c in Order.objects.filter(firm=firm_c).all():
            orders.append(ords_c)
        
    return render(request, 'orders.html', {'orders': orders, 'title':u'Изменение категории'})
svod_action.short_description = "Сводная"#заяввка

class FirmAdmin(ExportActionMixin,admin.ModelAdmin):
    actions = [svod_action, unfinished]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':40})},
    }
    resource_class = FirmResource
    list_filter = (('exp_date', DateRangeFilter),'ready', ('date', DateRangeFilter), 'report')
    list_display = ('title', 'text', 'count', 'date', 'exp_date', 'show_firm_url', status_colored, 'ready', 'readys', 'getouts', 'priems', 'printmkall','printpr', 'folder1', 'gant', 'assems')
    list_editable = ['count', 'date', 'exp_date', 'ready', 'text']
    search_fields = ['title']
    ordering = ['-date', 'exp_date']
    autocomplete_fields = ['assem', ]
    def show_firm_url(self, obj):
        #return format_html("{% url 'order' order_id=obj.id %}")
        verbose_name = 'Изделия(заказы)'
        verbose_name_plural = 'Изделия(заказы)'
        return format_html("<a href='/order/order/?firm__id__exact={url}'>Детали</a>", url=obj.pk)
    show_firm_url.short_description = 'Все детали'  
    
    def readys(self, obj):
        orders = Order.objects.filter(firm=obj).all().count()
        orders_ready = Order.objects.filter(firm=obj).filter(status='CM').all().count()
        if orders:
            result =  (orders_ready/orders)*100
            result = str(round(result,1))+'%'
        else: result='нет дет.'
        return result
    readys.short_description = "Готовность"
    def gant(self, obj):
        return format_html("<a href='/info/gantt?tool={url}&turnscnc=1&millscnc=1&turnunscnc=1&millunscnc=1'>gnt</a>", url=obj.id)
    gant.short_description = "График"
    def getouts(self, obj):
        return format_html("<a href='/order/getouts/{url}'>Выдача</a>", url=obj.id)
    getouts.short_description = "Выдача"
    def priems(self, obj):
        return format_html("<a href='/order/priems/{url}'>Прием</a>", url=obj.id)
    priems.short_description = "Прием"
    def assems(self, obj):
        t=''
        if obj.assem.all():
            for asms in obj.assem.all():
                t+=asms.title+'</br>'
        return format_html(t)
    assems.short_description = "Сборки"

    def printmkall(self, obj):
        url = '/order/printmkall'
        url = url + '/'+str(obj.id)
        return format_html('<a href="{}" class="button">&#128438;</a>', url)
    printmkall.short_description = "МК"

    def printpr(self, obj):
        url = '/order/printpr'
        url = url + '/'+str(obj.id)
        return format_html('<a href="{}" class="button">&#128438;</a>', url)
    printpr.short_description = "ПР"
    def folder1(self, obj):
        if obj.folder:
            url=obj.folder
            url= url.replace('"', '')
            url= url.replace('\\', '\\\\')
            return format_html('<button type="button" onclick="copyToClipboard(\' {} \')">  &dArr;  </button>', url,)
        return 'Нет'
    folder1.short_description = "folder"
    class Media:
        js = [
              'js/list_filter_collapse.js'
              ]
class AssemAdmin(admin.ModelAdmin):
    search_fields= ['title']
    list_display = ('title', 'text', 'tools')
    autocomplete_fields = ['tool', ]
    
    def tools(self, obj):
        t=''
        if obj.tool.all():
            for t_c in obj.tool.all():
                t+=str(t_c.title)+'</br>'
        return format_html(t)
    tools.short_description = "Детали"
    
    


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('content_type',)
    search_fields = ['user__username',]
    date_hierarchy = 'action_time'
admin.site.register(LogEntry, LogEntryAdmin)

admin.site.register(Firm, FirmAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Assem, AssemAdmin)
#admin.site.register(Orderformed, OrderformedAdmin)
