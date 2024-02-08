import mysite.asgi
from material.models import Material
from tools.models import Toolsonwarehouse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
tools=Toolsonwarehouse.objects.all()
for tool in tools:
    if tool.material:
        m, created = Material.objects.get_or_create(title = tool.material)
        tool.material_n=m
        tool.save()
    else:
        print(tool.title+'материал не указан')
    
    
    
