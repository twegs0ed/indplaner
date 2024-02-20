from django.db import models
from tools.models import Toolsonwarehouse
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils import timezone
from profiles.models import Machine


class Work(models.Model):
    tool = models.ForeignKey(Toolsonwarehouse,on_delete=models.CASCADE,null=True, verbose_name="Детали" )  
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Исполнитель")
    text = models.TextField(blank=True, null=True, verbose_name="Примечание" )#Описание
    date = models.DateField(default=timezone.now, verbose_name="Дата выполнения работы", null=True,blank=True)#Дата получения на склад
    time = models.TimeField(auto_now_add=True, verbose_name="Время")
    count = models.IntegerField(default=0, blank=True, null=True, verbose_name="Количество" ) # Количество инструмента на складе
    ready = models.BooleanField(default=True, verbose_name="Операция завршена и дальнейшие манипуляции с деталью на этой технологической операции не предусмотрены?" )
    machines = models.ManyToManyField(Machine, blank=True, null=True, verbose_name="Станки" )  
    def save(self, *args, **kwargs):
        
        super(Work, self).save(*args, **kwargs)
        self.machines.set(self.user.stanprofile.machines.all())

    class Meta:
        verbose_name = 'Выполненные работы'
        verbose_name_plural = 'Выполненные работы'


class WorkForm(ModelForm):
    
    class Meta:
        model = Work
        fields = ['tool', 'user','text','date','count', 'ready']
        #exclude = ['user']
    
    