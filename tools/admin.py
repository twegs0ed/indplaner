from django.contrib import admin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from .models import Toolsonwarehouse, Tools, Rec_Tools, Priem, Workplace, Norms
from profiles.models import Profile
from order.models import Order, Firm
from import_export.admin import ExportActionMixin, ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field
from django.utils.html import format_html
from import_export.widgets import ForeignKeyWidget, CharWidget, ManyToManyWidget
from django.db import models
from django.forms import TextInput, Textarea
import re
from material.models import Material
from django.shortcuts import render
import datetime
from work.models import Work
#import copy


def order_it(modeladmin, request, queryset):
    for obj in queryset:
        i=Order.get_count_ordered(obj)
        ord=Order()
        '''c_ord=get_object(Order,obj)
        if c_ord:
            c_ord.delete()'''
        ord.tool=obj
        ord.worker=Profile.objects.get(pk=10)
        ord.count=obj.min_count-obj.count-i
        ord.save()

def get_object(self, obj):
    try:
        return Order.objects.filter(tool=obj)
    except Order.DoesNotExist:
        return False


order_it.short_description = "В заявку"

class ToolsResource(resources.ModelResource):
    
   

    class Meta:
        model = Tools
        
        fields = ('tool__title', 'count','worker__bio', 'giveout_date')
        export_order = ('tool__title', 'worker__bio', 'count')

class ForeignKeyWidgetWithCreation (ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        try:
            return super(ForeignKeyWidgetWithCreation, self).clean(value, row, *args, **kwargs)
        except:
            return self.model.objects.create(**{self.field: value})
        
class ToolsonwarehouseResource(resources.ModelResource):
    material_n = Field(column_name='material_n',attribute='material_n',widget=ForeignKeyWidgetWithCreation(model=Material, field='title'))
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':40})},
    }
    #tool = Field(attribute='title', column_name='title', widget=CharWidget(),)
    similar = Field()
    workplace = Field(
        column_name='workplace',
        attribute='workplace',
        widget=ForeignKeyWidgetWithCreation(model=Workplace, field='name'))
    
    class Meta:
        model = Toolsonwarehouse
        #skip_unchanged=False
        fields = ('title', 'count', 'workplace__name','material_n' ,'similar','stock_sizes', 'count_in_one_stock', 'cover', 
                  'norm_lentopil_p','norm_lentopil','norm_plazma_p','norm_plazma','norm_turn_p','norm_turn','norm_mill_p',
                  'norm_mill','norm_turnun_p','norm_turnun','norm_millun_p',
                  'norm_millun','norm_electro_p','norm_electro','norm_slesarn','norm_sverliln_p','norm_sverliln','norm_rastoch_p','norm_rastoch')
        exclude = ('id',)
        export_order = ('title','count', 'workplace')
        import_id_fields=['title']
        #import_id_field = 'title'
    def dehydrate_similar(self, tool): 
        res=''
        if tool.id:
            if tool.similar:
                for t in tool.similar.all():
                    res+=t.title+', '
        return res

    
        
class ToolsonwarehouseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    formfield_overrides = {models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':40})},}
    exclude=['material']
    resource_class = ToolsonwarehouseResource
    autocomplete_fields = ['material_n', 'similar']
    list_display = ('title', 'count', 'workplace', 'created_date', 'text', 'cover', 'firms', 'material_n', 'similar_c')
    list_filter = ('workplace',)
    search_fields = ['title']
    ordering = ['title', 'created_date']
    list_editable = ['text']
    
    def get_search_results(self, request, queryset, search_term):
        search_term=str(search_term).upper()
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct
    def firms(self, obj):
        orders=Order.objects.filter(tool=obj)
        t=''
        f=[]
        for o in orders:
            if o.firm:
                f.append(o.firm.title)
            pass
        for x in f: 
            if f.count(x) > 1: 
                f.remove(x) 
        for x in f:
            t+=' <a href = "/order/order/?q='+x+'">'+x+'</a> '+'</br>'
            #t+=' <a href = "/tools/toolsonwarehouse/?q='+str(f.tool.title)+'">'+str(f.title)+'</a> '
        return format_html(t)
    firms.short_description = "Изделия"
    
    def similar_c(self,obj):
        res=''
        if obj.similar:
            for t in obj.similar.all():
                
                res+=' <a href = "/tools/toolsonwarehouse/'+str(t.id)+'">'+t.title+'</a> '+'</br>'+', '
        return format_html(res)
    similar_c.short_description = "Похожие"


class ToolsAdmin(ExportActionMixin, admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':40})},
    }
    #raw_id_fields = ('worker', 'tool')
    autocomplete_fields = ['tool','worker']
    resource_class = ToolsResource
    list_display = ('tool', 'worker', 'count', 'giveout_date', 'text','firms')
    list_filter = (('giveout_date', DateRangeFilter), 'worker')
    search_fields = ['tool__title', 'worker__bio']
    ordering = ['-giveout_date']
    list_editable = ['text']
    def get_search_results(self, request, queryset, search_term):
        #search_term=re.sub("[^\d\.]", "", str(search_term))
        search_term=str(search_term).upper()
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        #queryset |= self.model.objects.filter(tool__title=search_term)
        return queryset, use_distinct
    pass
    def firms(self, obj):
        orders=Order.objects.filter(tool=obj.tool).order_by('-order_date_worker')[:15]
        t=''
        f=[]
        for o in orders:
            if o.firm:
                f.append(o.firm.title)
            pass
        for x in f: 
            if f.count(x) > 1: 
                f.remove(x) 
        for x in f:
            t+=' <a href = "/order/order/?q='+x+'">'+x+'</a> '+'</br>'
            #t+=' <a href = "/tools/toolsonwarehouse/?q='+str(f.tool.title)+'">'+str(f.title)+'</a> '
        return format_html(t)
    firms.short_description = "Изделия"
class Rec_ToolsAdmin(ExportActionMixin, admin.ModelAdmin):
    #raw_id_fields = ('worker', 'tool')
    autocomplete_fields = ['worker', 'tool']
    resource_class = ToolsResource
    list_display = ('worker', 'tool', 'count', 'giveout_date')
    list_filter = (('giveout_date', DateRangeFilter), 'worker', 'tool')
    search_fields = ['tool__title', 'worker__bio']
    ordering = ['-giveout_date']
    pass
class ToolsdeficiteAdmin(admin.ModelAdmin):
    pass
class PriemResource(resources.ModelResource):
    firms = Field()
    tool = Field(
        column_name='tool',
        attribute='tool',
        widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='title'))
    #firm = Field(
        #column_name='firm',
        #attribute='firm',
        #widget=ForeignKeyWidgetWithCreation(model=Firm, field='title'))
    class Meta:
        model = Priem

        fields = ('tool', 'count','place','giveout_date','text', 'firms')
        export_order = ('tool', 'count')
        exclude = ('id',)
        import_id_fields = ('tool', 'count')
    def dehydrate_firms(self, obj):
        orders=Order.objects.filter(tool=obj.tool).order_by('-order_date_worker')[:15]
        t=''
        f=[]
        for o in orders:
            if o.firm:
                f.append(o.firm)
            pass
        for x in f: 
            if f.count(x) > 1: 
                f.remove(x) 
        for x in f:
            if x:
                t+=x.title+' - '+str(x.count)+' шт.'+'\n'
            #t+=' <a href = "/tools/toolsonwarehouse/?q='+str(f.tool.title)+'">'+str(f.title)+'</a> '
        return format_html(t)
    dehydrate_firms.short_description = "Изделия"
def svod_action(modeladmin, request, queryset):
    orders=[]
    firms = []
    #priems = queryset
    priems = list(queryset)
    for priem in priems:
        for pr in priems:
            if pr.tool==priem.tool and pr.giveout_date!=priem.giveout_date:
                priem.count+=pr.count
                priems.remove(pr)
    for priem in priems:
        for order_c in Order.objects.filter(tool=priem.tool).all():
            priem.c_count=priem.count
            orders.append([order_c, priem])
            if order_c.firm not in firms:
                if not order_c.firm:
                    break
                if not order_c.firm.exp_date:
                    order_c.firm.exp_date = datetime.date.today()
                firms.append(order_c.firm)


    firms = get_firms_for_priem(request, firms)
    orders_c = get_result_for_period(firms, priems)
    

    '''i=0
    for order in orders:
        print(order[0].tool,'-',order[0].count,'заказ')
        print(order[1].tool,'-',order[1].count,'прием')
        i+=1
        if i==5: break'''
        

    return render(request, 'priem.html', {'orders_c': orders_c,'orders': orders,'firms': firms,'title':u'Прием на склад'})
svod_action.short_description = "Сводная"#заяввка

def get_firms_for_priem(request, firms):
    start_date=datetime.datetime.strptime(request.GET.get('giveout_date__range__gte'), '%d.%m.%Y').date()
    end_date=datetime.datetime.strptime(request.GET.get('giveout_date__range__lte'), '%d.%m.%Y').date()
    firms.sort(key=lambda x: x.exp_date)
    firms = list(filter(lambda x: x.exp_date < (end_date+datetime.timedelta(40)), firms))
    firms = list(filter(lambda x: x.exp_date > (start_date-datetime.timedelta(40)), firms))
    return firms
def get_result_for_period(firms, priems):
    orders = []
    for firm in firms:
        for order in Order.objects.filter(firm=firm).all():
            orders.append(order)
            pass
    priems=list(priems)
    for priem in priems.copy():
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
                    #print(order.tool,order.percent, order.firm)
            
            break
        
    
    return orders

class PriemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    actions = [svod_action]
    resource_class = PriemResource
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':40})},
    } 
    autocomplete_fields = ['tool', 'place','worker']
    list_display = ('tool', 'count', 'giveout_date', 'text', 'firms')
    #list_filter = (('giveout_date', DateRangeFilter))
    list_filter = (('giveout_date', DateRangeFilter),)
    search_fields = ['tool__title']
    list_editable = ['text']
    def get_search_results(self, request, queryset, search_term):
        search_term=str(search_term).upper()
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        
        
        try:
            search_term_as_int = int(search_term)
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(tool=search_term_as_int)
        return queryset, use_distinct
    pass
    def firms(self, obj):
        orders=Order.objects.filter(tool=obj.tool)
        t=''
        f=[]
        for o in orders:
            if o.firm:
                f.append(o.firm.title)
            pass
        for x in f: 
            if f.count(x) > 1: 
                f.remove(x) 
        for x in f:
            t+=' <a href = "/order/order/?q='+x+'">'+x+'</a> '+'</br>'
            #t+=' <a href = "/tools/toolsonwarehouse/?q='+str(f.tool.title)+'">'+str(f.title)+'</a> '
        return format_html(t)
    firms.short_description = "Изделия"


class NormsResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        
        Toolsonwarehouse.objects.get_or_create(
            title=row.get('tool')
        )
    works = Field()
    tool = Field(column_name='tool',attribute='tool',widget=ForeignKeyWidget(model=Toolsonwarehouse, field='title'))
    
    #firm = Field(
        #column_name='firm',
        #attribute='firm',
        #widget=ForeignKeyWidgetWithCreation(model=Firm, field='title'))
    class Meta:
        model = Norms

        fields = ('tool', 'works',
                    'cncturn0','cncturn1', 'cncturn2','cncturn3','cncturn4','cncturn5','cncturn6','cncturn7',
                    'cncmill0','cncmill1','cncmill2','cncmill3','cncmill4','cncmill5','cncmill6','cncmill7',
                    'turn0','turn1', 'turn2','turn3','turn4','turn5','turn6','turn7',
                    'mill0','mill1','mill2','mill3','mill4','mill5','mill6','mill7',
                    'eroz0','eroz1','eroz2','eroz3','eroz4','eroz5','eroz6','eroz7',
                    'lentopil')
        #export_order = ('tool')
        import_id_fields = ('tool',)

        
        
    def dehydrate_works(self, obj):
        works = Work.objects.filter(tool=obj.tool).order_by('-date')[:2]
        t=''
        for o in works:
            t+=str(o.date)+' - '+str(o.count)+' шт. - '+o.user.get_full_name()+'-'
            #t+=' <a href = "/tools/toolsonwarehouse/?q='+str(f.tool.title)+'">'+str(f.title)+'</a> '
        return format_html(t)


class NormsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    #autocomplete_fields = ['tool','worker']
    resource_class = NormsResource
    list_display = ('tool', 'works',
                    'cncturn0','cncturn1', 'cncturn2','cncturn3','cncturn4','cncturn5','cncturn6','cncturn7',
                    'cncmill0','cncmill1','cncmill2','cncmill3','cncmill4','cncmill5','cncmill6','cncmill7',
                    'turn0','turn1', 'turn2','turn3','turn4','turn5','turn6','turn7',
                    'mill0','mill1','mill2','mill3','mill4','mill5','mill6','mill7',
                    'eroz0','eroz1','eroz2','eroz3','eroz4','eroz5','eroz6','eroz7',
                    'lentopil')
    #list_filter = (('giveout_date', DateRangeFilter), 'worker')
    search_fields = ['tool__title']
    #ordering = ['-giveout_date']
    #list_editable = ['text']
    def get_search_results(self, request, queryset, search_term):
        #search_term=re.sub("[^\d\.]", "", str(search_term))
        search_term=str(search_term).upper()
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        #queryset |= self.model.objects.filter(tool__title=search_term)
        return queryset, use_distinct
    pass
    def works(self, obj):
        works = Work.objects.filter(tool=obj.tool).order_by('-date')[:2]
        t=''
        for o in works:
            t+=str(o.date)+' - '+str(o.count)+' шт. - '+o.user.get_full_name()+'\n'
            #t+=' <a href = "/tools/toolsonwarehouse/?q='+str(f.tool.title)+'">'+str(f.title)+'</a> '
        return format_html(t)
    works.short_description = "Работы"

admin.site.register(Tools, ToolsAdmin)
admin.site.register(Priem, PriemAdmin)
admin.site.register(Norms, NormsAdmin)
admin.site.register(Toolsonwarehouse, ToolsonwarehouseAdmin)
#admin.site.register(Rec_Tools, Rec_ToolsAdmin)
