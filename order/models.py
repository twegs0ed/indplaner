from django.conf import settings
from django.db import models
from django.utils import timezone
from profiles.models import Profile
from tools.models import Toolsonwarehouse
from django.utils.html import format_html
from django import forms







class Firm(models.Model):
    title = models.CharField(max_length=200, verbose_name="Изделие" )#Наименование инструмента
    text = models.TextField(blank=True, null=True, verbose_name="Примечание" )#Описание
    #tools = models.ManyToManyField(Toolsonwarehouse)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Изделия(заказы)'
        verbose_name_plural = 'Изделия(заказы)'


class Order(models.Model):
    #worker = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Работник, которому заказывается инструмент")#Работник, который получил инструмент
    #tool = models.ForeignKey(Toolsonwarehouse,on_delete=models.CASCADE,null=True, verbose_name="Детали" )  # Работник, который получил инструмент
    tool = models.ForeignKey(Toolsonwarehouse,on_delete=models.CASCADE, blank=True ,null=True, verbose_name="Деталь")
    firm = models.ForeignKey(Firm,on_delete=models.CASCADE, blank=True ,null=True, verbose_name="Изделие(заказ)")
    text = models.TextField(blank=True, null=True, verbose_name="Примечание" )#Описание
    #created_date = models.DateTimeField(default=timezone.now, verbose_name="Дата выдачи" )#Дата получения на склад
    count = models.IntegerField(default=0, blank=True, null=True, verbose_name="Количество" ) # Количество инструмента на складе
    order_date_worker = models.DateTimeField(default=timezone.now, verbose_name="Дата запуска" )

    ORDERED_BY_WORKER = 'OW'
    ORDERED = 'OR'
    PAYED = 'PD'
    COM = 'CM'

    ORDER_CHOICES = [
        (ORDERED_BY_WORKER, 'В запуске'),
        (ORDERED, 'запущено'),
        (PAYED, 'на стороне'),
        (COM, 'изготовлено'),
    ]
    status = models.CharField(
        max_length=2,
        choices=ORDER_CHOICES ,
        default=ORDERED_BY_WORKER,
        verbose_name = 'статус',
        editable = False

    )

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    '''def save(self):
        self.tool.count-=self.count
        self.tool.save()
        return super(Tools, self).save()'''


    #def __str__(self):
        #return self.worker.username
        #return self.tool.title

    def worker_name(self):
        return self.worker.bio

    def get_count_ordered(obj):
        i = 0
        for e in Order.objects.all().filter(tool_id=obj.id).exclude(status=Order.COM):
            i = i + int(e.count or 0)
        return i

    class Meta:
        verbose_name = 'Детали по изделиям'
        verbose_name_plural = 'Детали по изделиям'

class Orderformed(models.Model):


    tools=models.ManyToManyField(Order, blank=True, null=True, verbose_name="Инструменты" )
    bill = models.TextField(blank=True, null=True, verbose_name="Номер счета" )#Описание
    text = models.TextField(blank=True, null=True, verbose_name="Примечание")  # Описание
    datetime = models.DateTimeField(default=timezone.now, verbose_name="Дата заказа" )
    status = models.CharField(
        max_length=2,
        choices=Order.ORDER_CHOICES,
        default=Order.ORDERED_BY_WORKER,
        verbose_name='статус',
        #editable=False

    )

    def get_tools(self):
        strt='<table>'
        for e in self.tools.all():
            strt = strt + "<tr><td><a href='/order/order/%s/change'>%s</a></td><td>%s шт.</td> <td> %s </td><td> %s</td> </tr>" % (e.id,e.tool, e.count, e.worker,  e.worker.workplace)
        return format_html(strt+'</table>')

    get_tools.short_description = "Заказанный инструмент"
    def __str__(self):
        return str(self.datetime)

    class Meta:
        verbose_name = 'Сформированные заказы'
        verbose_name_plural = 'Сформированные заказы'

    field_order = ['datetime']
class Get0rder():
    def getorder():
        return Order;
