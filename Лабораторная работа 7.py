import telebot
import psycopg2
from telebot import types
from datetime import datetime

conn = psycopg2.connect(database="forTGbot",
                        user="postgres",
                        password="iceVan731shtern",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

token = '5863765105:AAHZZFWHysZoQmtgoFd1SYSLEDQFC6l6DZE'
bot = telebot.TeleBot(token)
ping_counter = 0

days_list = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
week_number = datetime.today().isocalendar()[1] % 2


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    butn1 = types.KeyboardButton("Расписание на текущую неделю")
    butn2 = types.KeyboardButton("Расписание на следующую неделю")
    butn3 = types.KeyboardButton("Понедельник")
    butn4 = types.KeyboardButton("Вторник")
    butn5 = types.KeyboardButton("Среда")
    butn6 = types.KeyboardButton("Четверг")
    butn7 = types.KeyboardButton("Пятница")
    butn8 = types.KeyboardButton("Суббота")


    bot.send_message(message.chat.id, "Привет ,{first},Данный бот был создан для того,чтобы показать расписание МТУСИ."
                                      "\nВы можете ознакомится с возможностями данного бота, используя команду /help".format(first=message.from_user.first_name, reply_markup=keyboard))


@bot.message_handler(commands=['week'])
def weekNumber(message):
    if week_number == 1:
        bot.send_message(message.chat.id, "Сейчас  нечетная неделя")
    else:
        bot.send_message(message.chat.id, "Сейчас  четная неделя")





@bot.message_handler(commands=['help'])
def weekNumber(message):
    bot.send_message(message.chat.id, "Описание доступных команд:\n"
                                      "/help - Узнать команды бота\n"
                                      "/week - Узнать какая сейчас неделя (четная/нечетная) "
                                      "\n /cat - Выводит смешного кота "
                                      "\n /date - Узнать какая сейчас дата "
                                      "\n <Расписание на текущую неделю> -Узнать расписание на эту неделю "
                                      "\n <Расписание на следующую неделю> - Узнать расписание на будущую неделю"
                                      "\n <Понедельник - Суббота>  - Узнать расписание на определенный день")


@bot.message_handler(commands=['date'])
def date(message):
    bot.send_message(message.chat.id,"Дата    " + datetime.now().strftime("%y.%m.%d %H:%M:%S"))


@bot.message_handler(commands=['cat'])
def cat(message):
    bot.send_video(message.chat.id, 'https://tenor.com/ru/view/cat-the-cat-he-dance-he-dance-gif-24077288')
@bot.message_handler(content_types='text')
def reply(message):
    if message.text.lower() in days_list:
        if week_number == 1:
            cursor.execute(f"SELECT * FROM timetable where day = '{message.text.lower()} 1' or day = '{message.text.lower()} 0' order by start_time")
        else:
            cursor.execute(f"SELECT * FROM timetable where day = '{message.text.lower()} 2' or day = '{message.text.lower()} 0' order by start_time")
        records = list(cursor.fetchall())
        text = f"{message.text}:\n"
        text += '____________________________________________________________\n'
        for i in records:
            text += f"Предмет: {i[2]}; Кабинет: {i[3]}; Время: {i[4]} \n"
        text += "____________________________________________________________"
        bot.send_message(message.chat.id, text)
    elif 'текущую' in message.text.lower():
        text = ""
        for i in days_list:
            if week_number == 1:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 1' or day = '{i} 0' order by start_time")
            else:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 2' or day = '{i} 0' order by start_time")
            records = list(cursor.fetchall())
            text += f'{i.title()}:\n'
            text += '____________________________________________________________\n'
            if not records:
                text += "Выходной\n"
            for j in records:
                text += f"Предмет: {j[2]} Кабинет: {j[3]} Время: {j[4]}  \n"
            text += "____________________________________________________________"
            text += '\n\n'
        bot.send_message(message.chat.id, text)
    elif 'следующую' in message.text.lower():
        text = ""
        for i in days_list:
            if week_number + 1 == 1:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 1' or day = '{i} 0' order by start_time")
            else:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 2' or day = '{i} 0' order by start_time")
            records = list(cursor.fetchall())
            text += f'{i.title()}:\n'
            text += '____________________________________________________________\n'
            if not records:
                text += "Выходной\n"
            for j in records:
                text += f"Предмет: {j[2]} Кабинет: {j[3]} Время: {j[4]}  \n"
            text += "____________________________________________________________"
            text += '\n\n'
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "Извините, я Вас не понял")


bot.infinity_polling()
