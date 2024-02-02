import mysite.asgi
import datetime
import telebot;
from order.models import Order
from work.models import Work
bot = telebot.TeleBot('6532461428:AAFo13Xq6NAsy8y5JTlDJQsWFIy6HZE4IWA');
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    '''if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")'''
    orders=Order.objects.filter(tool__title__contains=message.text.upper()).order_by('-order_date_worker')[:10]
    if orders:
        for order in orders:
            t='*'+str(order.tool.title)+'*'+'-'+str(order.count)+'шт., запущено '+str(order.exp_date)
            t+='. '+'на складе '+str(order.tool.count)+'('+str(order.tool.workplace)+')'
            bot.send_message(message.from_user.id, t, parse_mode="Markdown")
    else:
        bot.send_message(message.from_user.id, "Не найдено")        
            
    works=Work.objects.filter(tool__title__contains=message.text.upper()).order_by('-date')[:15]
    if works:
        bot.send_message(message.from_user.id, 'Изготовление:')
        for work in works:
            t=''
            t+=str(work.user.first_name)+' '+str(work.user.last_name)+' - '+str(work.date)+'. Станки: '
            for  m in work.user.stanprofile.machines.all():
                t+=str(m.name)
            t+='. '+str(work.count)+' шт.'
            bot.send_message(message.from_user.id, t)
    else:
        bot.send_message(message.from_user.id, "Не изготавливалось")



bot.polling(none_stop=True, interval=0)