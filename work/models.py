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
    ready = models.BooleanField(default=True, verbose_name="Деталь готова?" )
    machines = models.ManyToManyField(Machine,  blank=True, null=True, verbose_name="Станки" )
    def save(self, *args, **kwargs):
		# set the value of the read_only_field using the regular field
        #self.machines = self.user.stanprofile.machines
        
		# call the save() method of the parent
        
        macs=self.user.stanprofile.machines.all()
        for item in macs:
            self.machines.add(item)
        super(Work, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Выполненные работы'
        verbose_name_plural = 'Выполненные работы'


class WorkForm(ModelForm):
    
    class Meta:
        model = Work
        fields = ['tool', 'user','text','date','count', 'ready', 'machines']
        #exclude = ['user']
    
    