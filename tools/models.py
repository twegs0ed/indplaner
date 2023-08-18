from django.conf import settings
from django.db import models
from django.utils import timezone, dateformat
from profiles.models import Profile
from workplace.models import Workplace
import order
from django.db.models import Q
from django.core.exceptions import ValidationError











class Toolsonwarehouse(models.Model):
    title = models.CharField(max_length=200, verbose_name="Обозначение" )#Наименование детали
    text = models.TextField(blank=True, null=True, verbose_name="Примечание" )#Описание
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Дата получения на склад" )#Дата получения на склад
    count = models.IntegerField(default=0,blank=True, null=True, verbose_name="Количество на складе" ) # Количество деталей на складе
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE, verbose_name="Место хранения", null=True, default=lambda: Workplace.objects.get(name='-'))#Работник, который получил детали
    
    #min_count = models.IntegerField(blank=True, null=True,verbose_name="Минимальное количество")  # Минимальное количество деталей на складе
    #need_count = models.IntegerField(blank=True, null=True,verbose_name="Дефицит")
    #ordered = models.ManyToManyField()
    


    def publish(self):
        self.published_date = timezone.now()
        self.save()


    #def save(self):
        #self.need_count = int(self.min_count or 0)-int(self.count or 0)
        #super(Toolsonwarehouse, self).save()


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Детали'
        verbose_name_plural = 'Детали на складе'


class Tools(models.Model):

    worker = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Работник")#Работник, который получил детали
    tool = models.ForeignKey(Toolsonwarehouse,on_delete=models.CASCADE,null=True, verbose_name="Деталь")  # Работник, который получил детали
    text = models.TextField(blank=True, null=True, verbose_name="Примечание" )#Описание
    #created_date = models.DateTimeField(default=timezone.now, verbose_name="Дата выдачи" )#Дата получения на склад
    count = models.IntegerField(default=0, null=True, verbose_name="Кол-во") # Количество деталей на складе
    giveout_date = models.DateTimeField(default=timezone.now, verbose_name="Дата выдачи" )
    is_cleaned=False


    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def save(self):
        if self.id is None:
            self.tool.count-=self.count
        else:
            #print(self.count)#что ввели
            count_c = self.count#сохраняем что ввели
            del self.count
            self.count#берем из базы
            count_cc = self.count#сохраняем из базы
            self.count = count_c#возвращаем то, что ввели
            #print(count_cc)
            #print(self.count)
            self.tool.count+=(count_cc-self.count)#новое значение = старое значение + (старое изменение - новое изменение
        self.tool.save()
        return super(Tools, self).save()
    def clean(self):
        if self.id is not None:
            count_c = self.count#сохраняем что ввели
            del self.count
            self.count#берем из базы
            count_cc = self.count#сохраняем из базы
            self.count = count_c#возвращаем то, что ввели
            if self.tool.count+(count_cc-self.count)<0:
                raise ValidationError(f"На складе недостаточно деталей({self.tool.count}) для выдачи указанного количества")
            if self.count<1:
                raise ValidationError(f"Отрицательное или нулевое количество")
        else:   
            if self.count<1:
                raise ValidationError(f"Отрицательное или нулевое количество")
            if self.count>self.tool.count:
                raise ValidationError(f"На складе недостаточно деталей({self.tool.count}) для выдачи указанного количества")
    def __str__(self):
        #return self.worker.username
        return self.worker.bio



    def worker_name(self):
        return self.worker.bio
    #def get_period(self):
        #return 'расходник' if self.tool.period == self.tool.SHORTPLAY else 'долгосрочный'

    #get_period.short_description = "Срок экспл."
    class Meta:
        verbose_name = 'Выдача'
        verbose_name_plural = 'Выдача деталей'


class Rec_Tools(models.Model):
    worker = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Работник")#Работник, который получил 
    tool = models.ForeignKey(Toolsonwarehouse,on_delete=models.CASCADE,null=True, verbose_name="Деталь" )  # Работник, который получил 
    text = models.TextField(blank=True, null=True, verbose_name="Примечание" )#Описание
    #created_date = models.DateTimeField(default=timezone.now, verbose_name="Дата выдачи" )#Дата получения на склад
    count = models.IntegerField(null=True, verbose_name="Кол-во" ) # Количество на складе
    giveout_date = models.DateTimeField(default=timezone.now, verbose_name="Дата сдачи" )




    def __str__(self):
        #return self.worker.username
        return self.worker.bio



    def worker_name(self):
        return self.worker.bio
    def get_period(self):
        return 'расходник' if self.tool.period == self.tool.SHORTPLAY else 'долгосрочный'

    get_period.short_description = "Срок экспл."
    class Meta:
        verbose_name = 'Брак'
        verbose_name_plural = 'Отбракованные детали'

class Priem(models.Model):
    def order_f(self):
        order_cf = order.models.Order.objects.filter(tool=self.tool).filter(
                Q(status=order.models.Order.ORDERED) | Q(status=order.models.Order.ORDERED_BY_WORKER) | Q(status=order.models.Order.PAYED)).order_by(
                'order_date_worker').first()
        if order_cf:
            if self.count<order_cf.count:
                order_cf.text=str(order_cf.text)+'\n'+dateformat.format(timezone.now(), 'd-m-Y')+" в запуске было "+str(order_cf.count)+"."
                order_cf.count-=self.count
                order_cf.status = order.models.Order.ORDERED
                order_cf.save()
            elif self.count==order_cf.count:
                order_cf.count=0
                order_cf.status = order.models.Order.COM  
                order_cf.save()
            else:
                order_cf.text='\n'+'Изготовлено '+dateformat.format(timezone.now(), 'd-m-Y')+' '+str(order_cf.count)+' шт. '
                diff=self.count-order_cf.count
                firm=order_cf.firm
                order_cf.count=0
                order_cf.status = order.models.Order.COM
                order_cf.save()

                
                order_cf=order.models.Order()
                order_cf.count=diff
                order_cf.tool=self.tool
                order_cf.text='Принято больше чем запущено(излишки) '+dateformat.format(timezone.now(), 'd-m-Y')
                order_cf.status = order.models.Order.COM
                order_cf.exp_date=timezone.now()
                order_cf.firm=firm
                order_cf.save()
                
            
        else:
            order_cf=order.models.Order()
            order_cf.count=self.count
            order_cf.tool=self.tool
            order_cf.text='Сформировано из "Приема"'
            order_cf.status = order.models.Order.COM
            order_cf.save()
   
        
        
    tool = models.ForeignKey(Toolsonwarehouse, on_delete=models.CASCADE, null=True, verbose_name="Детали")
    worker = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Работник, от которого принята деталь",null=True)
    count = models.IntegerField(null=True, verbose_name="Кол-во")
    place = models.ForeignKey(Workplace, on_delete=models.CASCADE, null=True, verbose_name="Место хранения")
    giveout_date = models.DateTimeField(default=timezone.now, verbose_name="Дата приема")
    text = models.TextField(blank=True, null=True, verbose_name="Примечание")  # Описание
    def save(self):

        if self.id is None:
            self.tool.count=int(self.tool.count or 0) + int(self.count or 0)
            if not self.tool.workplace==self.place:
                self.tool.text='Пред. место на '+dateformat.format(timezone.now(), 'd-m-Y')+' - '+str(self.tool.workplace)+'\n'+str(self.tool.text)
            self.tool.workplace=self.place
            
            Priem.order_f(self)
            #order_c.save()
        else:
            count_c = self.count  # сохраняем что ввели
            del self.count
            self.count  # берем из базы
            count_cc = self.count  # сохраняем из базы
            self.count = count_c  # возвращаем то, что ввели
            diff_count=self.count - count_cc# то, что ввели минус то, что в базе
            self.tool.count += diff_count  # новое значение = старое значение + (старое изменение - новое изменение///// то, что ввели - то, что в базе
            if not self.tool.workplace==self.place:
                self.tool.text='Пред. место на '+dateformat.format(timezone.now(), 'd-m-Y')+' - '+str(self.tool.workplace)+'\n'+str(self.tool.text)
            self.tool.workplace=self.place
        self.tool.save()
       
        return super(Priem, self).save()

    def __str__(self):
        return self.tool.title
    class Meta:
        verbose_name = 'прием'
        verbose_name_plural = 'прием деталей на склад'