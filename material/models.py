from django.db import models

# Create your models here.
class Material(models.Model):
    
    title = models.CharField(max_length=200, verbose_name="Изделие" )#Наименование инструмента
    text = models.TextField(blank=True, null=True, verbose_name="Примечание" )#Описание
    
    class Meta:
            verbose_name = 'Материал'
            verbose_name_plural = 'Материал'
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.title=self.title.upper()
        return super(Material, self).save(*args, **kwargs)