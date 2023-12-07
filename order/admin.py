from django.contrib import admin
from .models import Order, Firm, Orderformed
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from tools.models import Toolsonwarehouse
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
    

class OrderResource(resources.ModelResource):

    tool = Field(column_name='tool',attribute='tool',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='title'))
    firm = Field(column_name='firm',attribute='firm',widget=ForeignKeyWidgetWithCreation(model=Firm, field='title'))
    
    norm_lentopil_p = Field()
    norm_lentopil = Field()
    norm_plazma_p = Field()
    norm_plazma = Field()
    norm_turn_p = Field()
    norm_turn = Field()
    norm_mill_p = Field()
    norm_mill = Field()
    norm_millun_p = Field()
    norm_millun = Field()
    norm_electro_p = Field()
    norm_electro = Field()
    norm_slesarn = Field()
    norm_slesarn = Field()
    norm_sverliln_p = Field()
    norm_sverliln = Field()
    norm_rastoch_p = Field()
    norm_rastoch = Field()
    '''norm_lentopil_p = Field(column_name='norm_lentopil_p',attribute='norm_lentopil_p',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_lentopil_p'))
    norm_lentopil = Field(column_name='norm_lentopil',attribute='norm_lentopil',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_lentopil'))
    norm_plazma_p = Field(column_name='norm_plazma_p',attribute='norm_plazma_p',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_plazma_p'))
    norm_plazma = Field(column_name='norm_plazma',attribute='norm_plazma',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_plazma'))
    norm_turn_p = Field(column_name='norm_turn_p',attribute='norm_turn_p',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_turn_p'))
    norm_turn = Field(column_name='norm_turn',attribute='norm_turn',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_turn'))
    norm_mill_p = Field(column_name='norm_mill_p',attribute='norm_mill_p',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_mill_p'))
    norm_mill = Field(column_name='norm_mill',attribute='norm_mill',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_mill'))
    norm_millun_p = Field(column_name='norm_millun_p',attribute='norm_millun_p',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_millun_p'))
    norm_millun = Field(column_name='norm_millun',attribute='norm_millun',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_millun'))
    norm_electro_p = Field(column_name='norm_electro_p',attribute='norm_electro_p',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_electro_p'))
    norm_electro = Field(column_name='norm_electro',attribute='norm_electro',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_electro'))
    norm_slesarn = Field(column_name='norm_slesarn',attribute='norm_slesarn',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_slesarn'))
    norm_slesarn = Field(column_name='norm_slesarn',attribute='norm_slesarn',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_slesarn'))
    norm_sverliln_p = Field(column_name='norm_sverliln_p',attribute='norm_sverliln_p',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_sverliln_p'))
    norm_sverliln = Field(column_name='norm_sverliln',attribute='norm_sverliln',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_sverliln'))
    norm_rastoch_p = Field(column_name='norm_rastoch_p',attribute='norm_rastoch_p',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_rastoch_p'))
    norm_rastoch = Field(column_name='norm_rastoch',attribute='norm_rastoch',widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='norm_rastoch'))'''
       
    
    class Meta:
        model = Order
        fields = ('tool', 'count','exp_date', 'firm', 'status')
        
        export_order = ('tool', 'count', 'exp_date','firm')
        import_id_fields = ('tool','firm')
    def dehydrate_norm_lentopil_p(self, order): 
        if order.tool: return order.tool.norm_lentopil_p
        
            
        
    def dehydrate_norm_lentopil(self, order):  
        if order.tool: return order.count*order.tool.norm_lentopil
    def dehydrate_norm_plazma_p(self, order):  
        if order.tool: return order.tool.norm_plazma_p
    def dehydrate_norm_plazma(self, order):  
        if order.tool: return order.count*order.tool.norm_plazma
    def dehydrate_norm_turn_p(self, order):  
        if order.tool: return order.tool.norm_turn_p
    def dehydrate_norm_turn(self, order):  
        if order.tool: return order.count*order.tool.norm_turn
    def dehydrate_norm_mill_p(self, order):  
        if order.tool: return order.tool.norm_mill_p
    def dehydrate_norm_mill(self, order):  
        if order.tool: return order.count*order.tool.norm_mill
    def dehydrate_norm_turnun_p(self, order):  
        if order.tool: return order.tool.norm_turnun_p
    def dehydrate_norm_turnun(self, order):  
        if order.tool: return order.count*order.tool.norm_turnun
    def dehydrate_norm_millun_p(self, order):  
        if order.tool: return order.tool.norm_millun_p
    def dehydrate_norm_millun(self, order):  
        if order.tool: return order.count*order.tool.norm_millun
    def dehydrate_norm_electro_p (self, order):  
        if order.tool: return order.tool.norm_electro_p
    def dehydrate_norm_electro(self, order):  
        if order.tool: return order.count*order.tool.norm_electro
    def dehydrate_norm_slesarn(self, order):  
        if order.tool: return order.count*order.tool.norm_slesarn
    def dehydrate_norm_sverliln_p(self, order):  
        if order.tool: return order.tool.norm_sverliln_p
    def dehydrate_norm_sverliln(self, order):  
        if order.tool: return order.count*order.tool.norm_sverliln
    def dehydrate_norm_rastoch_p(self, order):  
        if order.tool: return order.tool.norm_rastoch_p
    def dehydrate_norm_rastoch(self, order):  
        if order.tool: return order.count*order.tool.norm_rastoch

            



class OrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':15})},
    }
    resource_class = OrderResource
    list_display = ('tool','count', 'c_count', 'status', 'firm', status_order_colored, 'exp_date','text', 'printmk', tool_cover, 'log', 'work', 'norms')
    list_filter = (('exp_date', DateRangeFilter),'status', 'firm')
    search_fields = ['tool__title', 'firm__title']
    ordering = ['tool__title']
    autocomplete_fields = [ 'tool', 'firm']
    actions = [make_ordered, make_payed, make_com, make_ordered_by_worker]
    list_editable = ['firm', 'count','exp_date', 'text', 'status']
    ordering = ['exp_date','-status']
    def printmk(self, obj):
        url = '/order/printmk'
        url = url + '/'+str(obj.id)
        return format_html('<a href="{}" class="button">&#128438;</a>', url)
    printmk.short_description = "МК"
    def norms(self, obj):
        t=''
        if obj.tool:
            t=str(obj.tool.title)+'</br>'
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
        js = ('js/guarded_admin.js',)
    




class FirmAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':40})},
    }
    list_display = ('title', 'text', 'count', 'date', 'exp_date', 'show_firm_url', status_colored)
    list_editable = ['count', 'date', 'exp_date']
    search_fields = ['title']
    ordering = ['-date', 'exp_date']
    def show_firm_url(self, obj):
        #return format_html("{% url 'order' order_id=obj.id %}")
        verbose_name = 'Изделия(заказы)'
        verbose_name_plural = 'Изделия(заказы)'
        return format_html("<a href='/order/order/?firm__id__exact={url}'>Детали</a>", url=obj.pk)
    show_firm_url.short_description = 'Все детали'  


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('content_type',)
    search_fields = ['user__username',]
    date_hierarchy = 'action_time'
admin.site.register(LogEntry, LogEntryAdmin)

admin.site.register(Firm, FirmAdmin)
admin.site.register(Order, OrderAdmin)
#admin.site.register(Orderformed, OrderformedAdmin)
