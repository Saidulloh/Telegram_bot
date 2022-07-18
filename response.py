# БОТ ДЛЯ ПЕРЕПИСКИ
import telebot
from telebot import types
import pyowm
import cities

owm = pyowm.OWM('5d3ff5ff43be72d71e13cba6accf2337')
bot = telebot.TeleBot('5010144656:AAHYq73VOqsbpv0hR3Bbq1wwz5nLzTr-Lwo')

name = ''
surname = ''
age = 0

# При введении start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,"Welcome!, Let's community!")
# При введении help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id,"Let's community!")
# Приветствие англ. вариант
priv = 'hello','Hello','hi','Hi','good morning','Good morning','good evening',\
    'Good evening','good night','Goof night','hey','Hey'
# Приветствие русс. вариант
privRus = 'Привет','привет','Здрасьте','здрасьте','Здравствуйте','здравствуйте',\
    'Прив','прив','Дарова','даров','добрый день','Добрый день','добрый вечер',\
    'Добрый вечер','Доброе утро','доброе утро'
# Прощание англ. вариант
prosh = 'bye','Bye','good bye','Good bye','see you','See you'
# Прощание русс. вариант
proshRus = 'пока','Пока','бывай','Бывай','Досвидание','досвидание','прощай','Прощай'
# Знакомство англ. вариант
znak = 'how are you?','How are you?',"What's up?","what's up?",'How are you doing?',\
    'how are you doing?',"How's it going?","how's it going?","How's life?","how's life?"
# Знакомство русс. вариант
znakRus = 'как дела?','Как дела?','как жизнь?','Как жизнь?' 
# Погода
def weather(message):
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(message.text)
    w = observation.weather
    temp = w.temperature('celsius')['temp']
        
    answer = f'In town {message.text} just {w.detailed_status} \n'
    answer += 'Temperature in district ' + str(temp)
    bot.send_message(message.chat.id, answer)

# Действия
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text in priv: # Приветствие англ. вариант
        bot.send_message(message.chat.id,'Hello:)')
    elif message.text in privRus: # Приветствие русс. вариант
        bot.send_message(message.chat.id,'Привет:)')
    elif message.text in prosh:
        bot.send_message(message.chat.id,'See u later!')
    elif message.text in proshRus:
        bot.send_message(message.chat.id,'Пока!')    
    elif message.text in znak:
        bot.send_message(message.chat.id,'Pretty good, and u?')
    elif message.text in znakRus:
        bot.send_message(message.chat.id,'Отлично, у вас как?')
    elif message.text in cities:
        weather(message.text) 
    elif message.text == "/reg":
        bot.send_message(message.chat.id,'Привет! Давай познакомимься. Как вас зовут?')
        bot.register_next_step_handler(message,reg_name)

def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.chat,'Какое у вас фамилие?')
    bot.register_next_step_handler(message,reg_surname)

def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.chat,'Сколько вам лет?')
    bot.register_next_step_handler(message,reg_age)

def reg_age(message):
    global age
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.chat.id,'Вводите цыфрами!')

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = f'Тебе {str(age)} лет? \nИ тебя зовут: {name} {surname}?'
    bot.send_message(message.chat.id, text = question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Приятно познакомиться! Теперь запишу в БД!")
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Попробуем еще раз!")
        bot.send_message(call.message.chat.id, "Привет! Давай познакомимся! Как тебя зовут?")
        bot.register_next_step_handler(call.message, reg_name)

bot.polling()