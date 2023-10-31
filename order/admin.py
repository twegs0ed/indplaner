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

class ForeignKeyWidgetWithCreation (ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        try:
            return super(ForeignKeyWidgetWithCreation, self).clean(value, row, *args, **kwargs)
        except:
            return self.model.objects.create(**{self.field: value})
    

class OrderResource(resources.ModelResource):
    tool = Field(
        column_name='tool',
        attribute='tool',
        widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='title'))
    firm = Field(
        column_name='firm',
        attribute='firm',
        widget=ForeignKeyWidgetWithCreation(model=Firm, field='title'))
    
    class Meta:
        model = Order
        fields = ('tool', 'count','exp_date', 'firm')
        export_order = ('tool', 'count')
        import_id_fields = ('tool','firm', 'exp_date')
def status_colored(obj):
    return mark_safe('<b style="background:{};">{}</b>'.format(obj.color,'______')+'<br><b style="background:{};">{}</b>'.format(obj.color2, '______'))
status_colored.allow_tags = True
status_colored.short_description = "Цвет"


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


class OrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':15})},
    }
    resource_class = OrderResource
    list_display = ('tool','count', 'status', 'firm', status_order_colored, 'exp_date','text', 'printmk', tool_cover, 'log')
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
    def log(self, obj):
        logs = LogEntry.objects.filter(content_type__app_label='order', object_id = obj.id).order_by('action_time').all()#or you can filter, etc.
        t=""
        for l in logs: 
            t+='<font color="green"><b>'+str(l.user)+'</b></font>'
            t+=" "
            if l.action_flag==1:t+="добавил "
            if l.action_flag==2:t+="изменил "
            if l.action_flag==3:t+="удалил "
            t+=datetime.strftime(l.action_time, '%d.%m.%Y')
            t+='<br>'

        return format_html(t)
    log.short_description = "История"
    
    class Media:
        css = {
            'all': (
                'css/fancy.css',
            )
        }
        js = ('js/guarded_admin.js',)
    


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('content_type',)
    search_fields = ['user__username',]
    date_hierarchy = 'action_time'
admin.site.register(LogEntry, LogEntryAdmin)

admin.site.register(Firm, FirmAdmin)
admin.site.register(Order, OrderAdmin)
#admin.site.register(Orderformed, OrderformedAdmin)
