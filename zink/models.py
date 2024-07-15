from django.conf import settings
from django.db import models
from django.utils import timezone, dateformat
from profiles.models import Profile
from workplace.models import Workplace
from material.models import Material
import order
from django.db.models import Q
from django.core.exceptions import ValidationError
import re
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from tools.models import Toolsonwarehouse



class Toolsonwarehousezn(models.Model):
    tool = models.ForeignKey(Toolsonwarehouse,on_delete=models.CASCADE, verbose_name="Деталь")
    count = models.IntegerField(default=0, null=True, verbose_name="Кол-во") # Количество деталей на складе
    workplace = models.ForeignKey(Workplace, blank=True, on_delete=models.CASCADE, verbose_name="Место хранения", null=True, )#Работник, который получил детали    
    text = models.TextField(blank=True, null=True, verbose_name="Примечание" )#Описание    

    def __str__(self):
        return self.tool.title

    class Meta:
        verbose_name = 'Детали'
        verbose_name_plural = 'Детали на складе'


class Toolszn(models.Model):

    worker = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Работник")#Работник, который получил детали
    tool = models.ForeignKey(Toolsonwarehousezn,on_delete=models.CASCADE,null=True, verbose_name="Деталь")  # Работник, который получил детали
    text = models.TextField(blank=True, null=True, verbose_name="Примечание" )#Описание
    #created_date = models.DateTimeField(default=timezone.now, verbose_name="Дата выдачи" )#Дата получения на склад
    count = models.IntegerField(default=0, null=True, verbose_name="Кол-во") # Количество деталей на складе
    giveout_date = models.DateTimeField(default=timezone.now, verbose_name="Дата выдачи" )
    and_priem = models.BooleanField(default=False, verbose_name="С приемом на склад" )
    is_cleaned=False
    order_count=0
    order_id=None


    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def save(self):
        #
        if self.and_priem:
            priem=Priemzn()
            
            priem.place = self.tool.workplace
            priem.tool=self.tool.tool
            priem.count=self.count
            priem.save()
            self.tool.count+=self.count



        if self.id is None:
            self.tool.count-=self.count
        else:
            c_t = Toolszn.objects.get(pk=self.id)
            workplace = self.tool.workplace
            self.tool.workplace = workplace
            self.tool.count = c_t.tool.count+(c_t.count - self.count)# на складе + (было - стало)




        
            
        self.tool.save()
        return super(Toolszn, self).save()
    def clean(self):
        if self.id:
            count_c = self.count#сохраняем что ввели
            del self.count
            self.count#берем из базы
            count_cc = self.count#сохраняем из базы
            self.count = count_c#возвращаем то, что ввели
            if self.tool.count+(count_cc-self.count)<0 and not self.and_priem:
                raise ValidationError(f"На складе недостаточно деталей({self.tool.count}) для выдачи указанного количества")
            if self.count<0:
                raise ValidationError(f"Отрицательное количество")
        else:   
            if self.count<1:
                raise ValidationError(f"Отрицательное или нулевое количество")
            if self.count>self.tool.count and not self.and_priem:
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




class Priemzn(models.Model):
        
    tool = models.ForeignKey(Toolsonwarehouse, on_delete=models.CASCADE, null=True, verbose_name="Детали")
    worker = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Работник, от которого принята деталь",null=True, blank=True)
    count = models.IntegerField(null=True, verbose_name="Кол-во")
    place = models.ForeignKey(Workplace, on_delete=models.CASCADE, null=True,  verbose_name="Место хранения", blank=True)
    giveout_date = models.DateTimeField(default=timezone.now, verbose_name="Дата приема")
    text = models.TextField(blank=True, null=True, verbose_name="Примечание")  # Описание
    def save(self):
        tool, t = Toolsonwarehousezn.objects.get_or_create(tool = self.tool)
        if not self.id:
            print('!!!!!!!!!',tool)
            tool.count+=int(self.count or 0)
            
            if not tool.workplace==self.place:
                tool.text='Пред. место на '+dateformat.format(timezone.now(), 'd-m-Y')+' - '+str(tool.workplace)+'\n'+str(tool.text)
            tool.workplace=self.place
            
            
            #order_c.save()
        else:#if self.id:
            
            pr=Priemzn.objects.get(pk=self.id)
            if pr:
                previous_count = pr.count
            else:
                previous_count=self.count
            
            diff_count=self.count - previous_count# то, что ввели минус то, что в базе. Если уменьшилось, то отрицательное
            self.tool.count +=  diff_count# новое значение = старое значение + (старое изменение - новое изменение///// то, что ввели - то, что в базе
            if not tool.workplace==self.place:
                tool.text='Пред. место на '+dateformat.format(timezone.now(), 'd-m-Y')+' - '+str(tool.workplace)+'\n'+str(tool.text)
            tool.workplace=self.place
            Priemzn.order_re(self, diff_count)
        tool.save()
       
        return super(Priemzn, self).save()

    def __str__(self):
        return self.tool.title
    class Meta:
        verbose_name = 'прием'
        verbose_name_plural = 'прием деталей на склад'

    
