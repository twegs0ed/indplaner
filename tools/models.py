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








class Toolsonwarehouse(models.Model):
    title = models.CharField(max_length=200, verbose_name="Обозначение" )#Наименование детали
    text = models.TextField(blank=True, null=True, verbose_name="Примечание" )#Описание
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Дата" )#Дата получения на склад
    count = models.IntegerField(default=0,blank=True, null=True, verbose_name="Количество на складе" ) # Количество деталей на складе
    workplace = models.ForeignKey(Workplace, blank=True, on_delete=models.CASCADE, verbose_name="Место хранения", null=True, )#Работник, который получил детали
    material = models.TextField(max_length=500, blank=True, null=True, verbose_name="Материал" )
    material_n = models.ForeignKey(Material, blank=True, on_delete=models.CASCADE, verbose_name="Материал", null=True, )#Работник, который получил детали
    stock_sizes = models.CharField(max_length=20, blank=True, null=True, verbose_name="Габариты заготовки" )
    count_in_one_stock = models.CharField(max_length=20, blank=True, null=True, verbose_name="Кол-во деталей из одной заготовки" )
    cover = models.BooleanField(default=False, verbose_name="Покрывается" )
    similar = models.ManyToManyField('self',blank=True, null=True, verbose_name="Похожие" )

    norm_lentopil_p = models.FloatField(default=0,blank=True, verbose_name="Ленточнопильная п/з, ч." )
    norm_lentopil = models.FloatField(default=0,blank=True, verbose_name="Ленточнопильная, ч." )
    
    norm_plazma_p = models.FloatField(default=0,blank=True, verbose_name="Плазма п/з, ч." )
    norm_plazma = models.FloatField(default=0,blank=True, verbose_name="Плазма, ч." )

    norm_turn_p = models.FloatField(default=0,blank=True, verbose_name="Токарная ЧПУ п/з, ч." )
    norm_turn = models.FloatField(default=0,blank=True, verbose_name="Токарная ЧПУ, ч." )

    norm_turnun_p = models.FloatField(default=0,blank=True, verbose_name="Токарная универс. п/з, ч." )
    norm_turnun = models.FloatField(default=0,blank=True, verbose_name="Токарная универс., ч." )


    norm_mill_p = models.FloatField(default=0,blank=True, verbose_name="Фрезерная ЧПУ п/з, ч." )
    norm_mill = models.FloatField(default=0,blank=True, verbose_name="Фрезерная ЧПУ, ч." )

    norm_millun_p = models.FloatField(default=0,blank=True, verbose_name="Фрезерная универс. п/з, ч." )
    norm_millun = models.FloatField(default=0,blank=True, verbose_name="Фрезерная универс. , ч." )

    norm_electro_p = models.FloatField(default=0,blank=True, verbose_name="Электроэрозионная п/з, ч." )
    norm_electro = models.FloatField(default=0,blank=True, verbose_name="Электроэрозионная, ч." )


    norm_slesarn = models.FloatField(default=0,blank=True, verbose_name="Слесарная, ч." )


    norm_sverliln_p = models.FloatField(default=0,blank=True, verbose_name="Сверлильная п/з, ч." )
    norm_sverliln = models.FloatField(default=0,blank=True, verbose_name="Сверлильная, ч." )


    norm_rastoch_p = models.FloatField(default=0,blank=True, verbose_name="Расточная п/з, ч." )
    norm_rastoch = models.FloatField(default=0,blank=True, verbose_name="Расточная, ч." )



    def publish(self):
        self.published_date = timezone.now()
        self.save()

 

    def save(self, *args, **kwargs):
        
        ts=[]
        ts.append(self)
        


        if self.id is None:
            self.title=self.title.upper()
            return super(Toolsonwarehouse, self).save(*args, **kwargs)
        else:
            for t in self.similar.all():
                ts.append(t)

            for t in ts:
                
                for t_c in ts:
                    t.similar.add(t_c)
            self.title=self.title.upper()
            return super(Toolsonwarehouse, self).save(*args, **kwargs)
    

        #self.need_count = int(self.min_count or 0)-int(self.count or 0)
        #super(Toolsonwarehouse, self).save()
    def clean(self):
        #title_c=self.title.split (' ',1)[0]
        if Toolsonwarehouse.objects.filter(title__contains=self.title.upper()).exclude(id=self.id).exists():
            raise ValidationError('Такие детали уже есть в базе')
        t=self.title.upper()
        if t!=self.title.upper():
            raise ValidationError(f"Названия должны быть прописными буквами({self.tool.title})")
        if self.count<0:
                raise ValidationError(f"Отрицательное количество")
    
        
        

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
            priem=Priem()
            priem.tool=self.tool
            priem.count=self.count
            priem.save()



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
        if self.id:
            count_c = self.count#сохраняем что ввели
            del self.count
            self.count#берем из базы
            count_cc = self.count#сохраняем из базы
            self.count = count_c#возвращаем то, что ввели
            if self.tool.count+(count_cc-self.count)<0 and not self.and_priem:
                raise ValidationError(f"На складе недостаточно деталей({self.tool.count}) для выдачи указанного количества")
            if self.count<1:
                raise ValidationError(f"Отрицательное или нулевое количество")
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
            safe_self_count = self.count
            while self.count > order_cf.count:
                #сохраним количество деталей приема для дальнейцшегно восстановления значения
                self.count-=order_cf.count
                order_cf.status = order.models.Order.COM  
                order_cf.save()
                order_cf = order.models.Order.objects.filter(tool=self.tool).filter(
                Q(status=order.models.Order.ORDERED) | Q(status=order.models.Order.ORDERED_BY_WORKER) | Q(status=order.models.Order.PAYED)).order_by(
                'order_date_worker').first()
                if order_cf == None:
                    order_cf=order.models.Order()
                    order_cf.count=self.count
                    order_cf.tool=self.tool
                    order_cf.text='Сформировано из "Приема"'
                    order_cf.status = order.models.Order.COM
                    order_cf.save()
                    self.count = safe_self_count
                    return 1
            if self.count<order_cf.count:
                order_cf1 = order_cf
                order_cf.text=str(order_cf.text)+'\n'+dateformat.format(timezone.now(), 'd-m-Y')+" в запуске было "+str(order_cf.count)+"."
                order_cf.count-=self.count
                order_cf.order_date_worker=timezone.now()
                order_cf.save()

                users=User.objects.all()
                mails=[]
                for u in users:
                    if u.groups.filter(name='tehnolog').exists():
                        if u.email:
                            mails.append(u.email)
                send_mail(
                'Прием деталей на склад',
                'Деталь: '+order_cf.tool.title+
                '\nИзделие: '+str(order_cf.firm),
                settings.EMAIL_FROM_ADRESS,
                mails,
                fail_silently=False,
            )
                order_cf1.pk = None
                order_cf1.count = self.count
                order_cf1.status = order.models.Order.COM
                order_cf1.save()
                self.count = safe_self_count
                return 1
            elif self.count==order_cf.count:
                #order_cf.count=0
                order_cf.status = order.models.Order.COM  
                order_cf.save()
                self.count = safe_self_count
        else:
            order_cf=order.models.Order()
            order_cf.count=self.count
            order_cf.tool=self.tool
            order_cf.text='Сформировано из "Приема"'
            order_cf.status = order.models.Order.COM
            order_cf.save()
   
        
        
    tool = models.ForeignKey(Toolsonwarehouse, on_delete=models.CASCADE, null=True, verbose_name="Детали")
    worker = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Работник, от которого принята деталь",null=True, blank=True)
    count = models.IntegerField(null=True, verbose_name="Кол-во")
    place = models.ForeignKey(Workplace, on_delete=models.CASCADE, null=True,  verbose_name="Место хранения", blank=True)
    giveout_date = models.DateTimeField(default=timezone.now, verbose_name="Дата приема")
    text = models.TextField(blank=True, null=True, verbose_name="Примечание")  # Описание
    def save(self):

        if self.id is None:
            '''
            title_c=self.tool.title.split (' ',1)[0]
            alltools = Toolsonwarehouse.objects.filter(Q(title__icontains=title_c.lower()) | Q(title__icontains=title_c.upper()))
            count_all=0
            if alltools:
                for item in alltools:
                    count_all+=int(item.count or 0)
                    if not item.pk == self.tool.pk:
                        self.tool.text='Пред. место на '+dateformat.format(timezone.now(), 'd-m-Y')+' - '+str(item.workplace)+'\n'+str(self.tool.text)
                        for v in Tools.objects.filter(tool=item):
                            v.tool=self.tool
                            v.save()
                        for p in Priem.objects.filter(tool=item):
                            if not p == self:
                                p.tool=self.tool
                                p.save()
                        item.delete()
                        '''
            self.tool.count+=int(self.count or 0)
            
            if not self.tool.workplace==self.place:
                self.tool.text='Пред. место на '+dateformat.format(timezone.now(), 'd-m-Y')+' - '+str(self.tool.workplace)+'\n'+str(self.tool.text)
            self.tool.workplace=self.place
            
            Priem.order_f(self)
            
            #order_c.save()
        else:
            '''
            title_c=self.tool.title.split (' ',1)[0]
            alltools = Toolsonwarehouse.objects.filter(Q(title__icontains=title_c.lower()) | Q(title__icontains=title_c.upper()))
            count_all=0
            if alltools:
                for item in alltools:
                    count_all+=int(item.count or 0)
                    if not item.pk == self.tool.pk:
                        self.tool.text='Пред. место на '+dateformat.format(timezone.now(), 'd-m-Y')+' - '+str(item.workplace)+'\n'+str(self.tool.text)
                        for v in Tools.objects.filter(tool=item):
                            v.tool=self.tool
                            v.save()
                        
                            
                        item.delete()
                        '''
            pr=Priem.objects.filter(pk=self.id).first()
            if pr:
                previous_count = pr.count
            else:
                previous_count=self.count
            
            diff_count=self.count - previous_count# то, что ввели минус то, что в базе
            self.tool.count +=  diff_count# новое значение = старое значение + (старое изменение - новое изменение///// то, что ввели - то, что в базе
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