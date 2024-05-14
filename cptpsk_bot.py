import mysite.asgi
import datetime
import telebot;
from order.models import Order
from work.models import Work
import subprocess
import os

bot = telebot.TeleBot('6532461428:AAFo13Xq6NAsy8y5JTlDJQsWFIy6HZE4IWA');
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    
    orders=Order.objects.filter(tool__title__contains=message.text.upper()).filter(firm__report=False).order_by('-order_date_worker')[:6]
    bot.send_message(message.from_user.id, "*Запуск:*", parse_mode="Markdown") 
    if orders:
        for order in orders:
            t=' '+str(order.tool.title)+' '+'-*'+str(order.count)+' шт.*, \nзапущено: '+str(order.order_date_worker)+' срок: '+str(order.exp_date)
            t+='. '+' \nна складе '+str(order.tool.count)+'('+str(order.tool.workplace)+')'
            t+=' \nИзделие:*'+order.firm.title+' - '+str(order.firm.count)+'шт.'+'*.\n'
            t+=order.get_status()
            bot.send_message(message.from_user.id, t, parse_mode="Markdown")
    else:
        bot.send_message(message.from_user.id, "Не найдено запуска")        
            
    works=Work.objects.filter(tool__title__contains=message.text.upper()).order_by('-date')[:8]
    if works:
        bot.send_message(message.from_user.id, '*Изготовление:*', parse_mode="Markdown")
        for work in works:
            t=''
            t+=str(work.user.first_name)+' '+str(work.user.last_name)+' - '+str(work.date)+'.\nСтанки: '
            for  m in work.user.stanprofile.machines.all():
                t+=str(m.name)
            t+='. '+str(work.count)+' шт.'
            bot.send_message(message.from_user.id, t)
    else:
        bot.send_message(message.from_user.id, "Не изготавливалось")
    f_c=find_files(message.text)
    
    if f_c:
        bot.send_message(message.from_user.id, f_c)
        bot.send_document(message.from_user.id,open(f_c, 'rb'))
    else:
        bot.send_message(message.from_user.id, "документ не найден")

def find_files(name):
    for root, dirs, files in os.walk('N:\Home\АРХИВ'):
        for file in files:
            
            if name in file and file.endswith('.pdf'):
                if 'АРХИВНЫЙ ЭКЗЕМПЛЯР' in root: continue
                return str(os.path.join(root, file))
    for root, dirs, files in os.walk('N:\Home\Электронное КД\Перетяжка'):
        for file in files:
            if name in file and file.endswith('.pdf'):
                if 'АРХИВНЫЙ ЭКЗЕМПЛЯР' in root: continue
                return str(os.path.join(root, file))
    for root, dirs, files in os.walk('N:\Vol_Work\Иванов ВВ\КТО'):
        for file in files:
            if name in file and file.endswith('.pdf'):
                if 'АРХИВНЫЙ ЭКЗЕМПЛЯР' in root: continue
                return str(os.path.join(root, file))
    return 0


'''def find_files(file_name=None):



    path = 'H:\music'
    for dirs,folder,files in os.walk(path):
        print('Выбранный каталог: ', dirs)
        print('Вложенные папки: ', folder)
        print('Файлы в папке: ', files)
        print('Полный путь к файлу: ', os.path.join(dirs, files))
        for f in files:
            return os.path.join(dirs, f)'''

bot.polling(none_stop=True, interval=0)