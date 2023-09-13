from django.db import models
from tools.models import Toolsonwarehouse
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils import timezone








class Work(models.Model):
    
    tool = models.ForeignKey(Toolsonwarehouse,on_delete=models.CASCADE,null=True, verbose_name="Детали" )  # Работник, который получил инструмент
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Исполнитель")
    text = models.TextField(blank=True, null=True, verbose_name="Примечание" )#Описание
    date = models.DateField(default=timezone.now, verbose_name="Дата выполнения работы", null=True,blank=True)#Дата получения на склад
    count = models.IntegerField(default=0, blank=True, null=True, verbose_name="Количество" ) # Количество инструмента на складе

    class Meta:
        verbose_name = 'Выполненные работы'
        verbose_name_plural = 'Выполненные работы'


class WorkForm(ModelForm):
    class Meta:
        model = Work
        fields = ['tool', 'user','text','date','count']
    
    