from django.db import models
from tools.models import Toolsonwarehouse, Norms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils import timezone
from profiles.models import Machine


class Work(models.Model):
    NUMB_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
    )
    tool = models.ForeignKey(Toolsonwarehouse,on_delete=models.CASCADE,null=True, verbose_name="Детали" )  
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Исполнитель")
    text = models.TextField(blank=True, null=True, verbose_name="Примечание" )#Описание
    date = models.DateField(default=timezone.now, verbose_name="Дата выполнения работы", null=True,blank=True)#Дата получения на склад
    time = models.TimeField(auto_now_add=True, verbose_name="Время")
    work_time = models.IntegerField(null=True,blank=True, verbose_name="Время на одну дет., мин")
    count = models.IntegerField(default=0, blank=True, null=True, verbose_name="Количество" ) # Количество инструмента на складе
    ready = models.BooleanField(default=True, verbose_name="Опер. завершена?" )
    machines = models.ManyToManyField(Machine, blank=True, null=True, verbose_name="Станки" )  
    numb_ust = models.IntegerField(default=0, blank=False, null=False, verbose_name="Номер установа", choices=NUMB_CHOICES) # 

    def save(self, *args, **kwargs):
        setnormstotool(self.tool, self)
        for t_c in self.tool.similar.all():
            print(t_c.title)
            setnormstotool(t_c, self)

            pass
        
        super(Work, self).save(*args, **kwargs)
        self.machines.set(self.user.stanprofile.machines.all())

    class Meta:
        verbose_name = 'Выполненные работы'
        verbose_name_plural = 'Выполненные работы'


class WorkForm(ModelForm):
    
    class Meta:
        model = Work
        fields = ['tool', 'user','text','date','count', 'ready', 'work_time', 'numb_ust']
        #exclude = ['user']
def setnormstotool(tool, self):
    try:
            norms, _ = Norms.objects.get_or_create(tool = tool)
            

    except Norms.MultipleObjectsReturned:
        norms = Norms.objects.filter(tool = tool).first()
        
        pass
    if self.work_time:
        if self.user.stanprofile.operation:
            if self.user.stanprofile.operation.name =='Фрезерная с ЧПУ':
                if self.numb_ust==0:norms.cncmill0 = self.work_time
                elif self.numb_ust==1:norms.cncmill1 = self.work_time
                elif self.numb_ust==2:norms.cncmill2 = self.work_time
                elif self.numb_ust==3:norms.cncmill3 = self.work_time
                elif self.numb_ust==4:norms.cncmill4 = self.work_time
                elif self.numb_ust==5:norms.cncmill5 = self.work_time
                elif self.numb_ust==6:norms.cncmill6 = self.work_time
                elif self.numb_ust==7:norms.cncmill7 = self.work_time
            elif self.user.stanprofile.operation.name =='Токарная с ЧПУ':
                if self.numb_ust==0:norms.cncturn0 = self.work_time
                elif self.numb_ust==1:norms.cncturn1 = self.work_time
                elif self.numb_ust==2:norms.cncturn2 = self.work_time
                elif self.numb_ust==3:norms.cncturn3 = self.work_time
                elif self.numb_ust==4:norms.cncturn4 = self.work_time
                elif self.numb_ust==5:norms.cncturn5 = self.work_time
                elif self.numb_ust==6:norms.cncturn6 = self.work_time
                elif self.numb_ust==7:norms.cncturn7 = self.work_time
            elif self.user.stanprofile.operation.name =='Фрезерная универсальная':
                if self.numb_ust==0:norms.mill0 = self.work_time
                elif self.numb_ust==1:norms.mill1 = self.work_time
                elif self.numb_ust==2:norms.mill2 = self.work_time
                elif self.numb_ust==3:norms.mill3 = self.work_time
                elif self.numb_ust==4:norms.mill4 = self.work_time
                elif self.numb_ust==5:norms.mill5 = self.work_time
                elif self.numb_ust==6:norms.mill6 = self.work_time
                elif self.numb_ust==7:norms.mill7 = self.work_time
            elif self.user.stanprofile.operation.name =='Токарная универсальная':
                if self.numb_ust==0:norms.turn0 = self.work_time
                elif self.numb_ust==1:norms.turn1 = self.work_time
                elif self.numb_ust==2:norms.turn2 = self.work_time
                elif self.numb_ust==3:norms.turn3 = self.work_time
                elif self.numb_ust==4:norms.turn4 = self.work_time
                elif self.numb_ust==5:norms.turn5 = self.work_time
                elif self.numb_ust==6:norms.turn6 = self.work_time
                elif self.numb_ust==7:norms.turn7 = self.work_time
            elif self.user.stanprofile.operation.name =='Электроэрозионная':
                if self.numb_ust==0:norms.eroz0 = self.work_time
                elif self.numb_ust==1:norms.eroz1 = self.work_time
                elif self.numb_ust==2:norms.eroz2 = self.work_time
                elif self.numb_ust==3:norms.eroz3 = self.work_time
                elif self.numb_ust==4:norms.eroz4 = self.work_time
                elif self.numb_ust==5:norms.eroz5 = self.work_time
                elif self.numb_ust==6:norms.eroz6 = self.work_time
                elif self.numb_ust==7:norms.eroz7 = self.work_time
            elif self.user.stanprofile.operation.name =='Ленточнопильная':
                norms.lentopil = self.work_time
    norms.save()
    
    