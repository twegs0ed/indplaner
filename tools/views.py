from django.shortcuts import render
from django.utils import timezone
from .models import Toolsonwarehouse
from django.http import HttpResponse


def tools_list(request):
    tools= Toolsonwarehouse.objects.all().order_by('-created_date')
    return render(request, 'tools/tools_list.html', {'tools': tools})

def tool_detail(request, pk):
    tool=Toolsonwarehouse.objects.get(pk=pk)
    #tool = get_object_or_404(Toolsonwarehouse, pk=pk)
    return render(request, 'tools/tool_detail.html', {'tool': tool})
