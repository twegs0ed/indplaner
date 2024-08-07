from django.shortcuts import render

# Create your views here.
def printm15(request, id):
    first_name = [x+'.' for x in request.user.first_name if x.isupper()]
    fio = request.user.last_name+' '+''.join(first_name)
    order=Order.objects.get(pk=id)
    wb = load_workbook(filename = 'static/xls/M15.xlsx')
    ws = wb.active
    ws.cell(row=21, column=8).value=str(fio)

    if order.firm != None:
        ws.cell(row=2, column=2).value=str(order.firm)
    else:
        ws.cell(row=2, column=2).value=' '
    ws.cell(row=3, column=2).value=str(order.tool)
    if order.exp_date != None:
        ws.cell(row=4, column=2).value= format(order.exp_date, '%d.%m.%Y')
    else:
        ws.cell(row=4, column=2).value= ' '
    if order.tool.material_n != None:
        ws.cell(row=3, column=7).value= str(order.tool.material_n)
    else:
        ws.cell(row=3, column=7).value= ' '
    if order.tool.stock_sizes != None:
        ws.cell(row=4, column=7).value= str(order.tool.stock_sizes)
    else:
        ws.cell(row=4, column=7).value= ' '
    if order.tool.count_in_one_stock != None:
        count_cc = count_c(int(float(order.count)),int(float(order.tool.count_in_one_stock)), order.tool.stock_sizes, ws)
        ws=count_cc['ws']
        ws.cell(row=5, column=7).value= count_cc['count']
    else:
        ws.cell(row=5, column=7).value= ' '


    ws.cell(row=5, column=2).value=str(order.count)
    name = str(uuid.uuid4())
    
    image = qrcode.make(request.META['HTTP_HOST']+'/work/work/add/'+str(order.tool.id))
    
    image.save('static/xls/'+name+'.gif')# Напишите здесь свой код :-)


    img = openpyxl.drawing.image.Image('static/xls/'+name+'.gif')
    img.height = 150
    img.width = 150
    img.anchor = 'A24' # Or whatever cell location you want to use.
    ws.add_image(img)
    
   
    #ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=4)
    wb.save('static/xls/'+name+'.xlsx')

    file = io.open('static/xls/'+name+'.xlsx', "rb", buffering = 1024*256)
    file.seek(0)
    response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename= '+name+'.xlsx'
    
    file.close()
    if os.path.isfile('static/xls/'+name+'.xlsx'): os.remove('static/xls/'+name+'.xlsx')
    if os.path.isfile('static/xls/'+name+'.gif'): os.remove('static/xls/'+name+'.gif')

    return response