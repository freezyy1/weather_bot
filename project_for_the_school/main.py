# для установки необходимых библиотек введите в консоль следующее: 
# pip install telebot
# pip install requests
import requests
import telebot
# импортируем данные для работы бота
from tokens import url, api_weather, api_telegram

bot = telebot.TeleBot(api_telegram)

# ниже представлен набор команд, которые умеет обрабатывать бот
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Добро пожаловать, ' + str(message.from_user.first_name) + ',' + '\n' +
                     'чтобы узнать погоду напишите в чат название города')


@bot.message_handler(commands=['help'])
def welcome(message):
    bot.send_message(message.chat.id,
                     '/start - запуск бота\n/help - команды бота\nчтобы узнать погоду напишите в чат название города')


@bot.message_handler(content_types=['text'])
def test(message):
    try:
        # создаем глобальные переменные чтобы не было проблем с выводом локальных переменных в будущем
        global wind
        global temp

        city_name = message.text

        params = {'APPID': api_weather, 'q': city_name, 'units': 'metric', 'lang': 'ru'}
        result = requests.get(url, params=params)
        weather = result.json()

        # условие для температуры воздуха
        if weather["main"]['temp'] < 10:
            temp = "Сейчас холодно"
        elif weather["main"]['temp'] < 20:
            temp = "Сейчас прохладно"
        elif weather["main"]['temp'] > 30:
            temp = "Сейчас жарко"

        # условие для скорости ветра
        if weather["wind"]['speed'] == 0:
            wind = "По шкале Бофорта сейчас Штиль"
        elif 1.5 >= weather["wind"]['speed'] >= 0.5:
            wind = "По шкале Бофорта сейчас тихий ветер "
        elif 1.6 <= weather["wind"]['speed'] <= 3.3:
            wind = "По шкале Бофорта сейчас легкий ветер"
        elif 3.4 <= weather["wind"]['speed'] <= 5.4:
            wind = "По шкале Бофорта сейчас слабый ветер"
        elif 5.5 <= weather["wind"]['speed'] <= 7.9:
            wind = "По шкале Бофорта сейчас умеренный ветер"
        elif 8.0 <= weather["wind"]['speed'] <= 10.7:
            wind = "По шкале Бофорта сейчас свежий ветер"
        elif 10.8 <= weather["wind"]['speed'] <= 13.8:
            wind = "По шкале Бофорта сейчас сильный ветер"

        bot.send_message(message.chat.id,
                         "В городе " + str(weather["name"]) + " температура: " + str(
                             int(weather["main"]['temp'])) + '°' + "\n" +
                         "Максимальная температура: " + str(int(weather['main']['temp_max'])) + "\n" +
                         "Минимальная температура: " + str(int(weather['main']['temp_min'])) + "\n" +
                         "Скорость ветра: " + str(int(weather['wind']['speed'])) + ' м/c' + "\n" +
                         "Давление: " + str(int(weather['main']['pressure'])) + 'мм рт. ст.' + "\n" +
                         "Влажность: " + str(int(weather['main']['humidity'])) + "%" + "\n" +
                         "Видимость: " + str(weather['visibility']) + "\n" +
                         "Описание: " + str(weather['weather'][0]["description"]) + "\n" + temp + "\n" + wind + '\n')
    except:
        bot.send_message(message.chat.id, 'вы ввели город, которого нет в базе данных \n')
        bot.send_message(message.chat.id, 'рестарт... \n')
        bot.send_message(message.chat.id, 'введите название города')


bot.polling(none_stop=True)
