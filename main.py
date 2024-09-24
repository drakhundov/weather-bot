import os

import requests
import telebot

URL = (
    "https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid="
    + os.getenv("API_TOKEN")
)

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))


@bot.message_handler(commands=["start"])
def start(message):
    first_message = "<b> Hi!\nEnter place, please. </b>"
    bot.send_message(message.chat.id, first_message, parse_mode="html")


@bot.message_handler(content_types=["text"])
def send_info(message):
    user_message = message.text.strip().lower()

    if user_message == "hello" or user_message == "hi":
        start(message)
    else:
        bot.send_message(message.chat.id, weather(user_message))


def weather(place):
    try:
        info = requests.get(URL.format(city=place)).json()

        desc = info["weather"][0]["description"]
        temp = info["main"]["temp"]

        status = (
            "It is "
            + desc
            + " in "
            + " ".join([i.capitalize() for i in place.split(" ")])
            + " now.\n"
        )
        status += "Temperature now is " + str(temp) + " degrees.\n"

        if temp > 25:
            status += "Wear shorts (or skirt) and a T-shirt."
        elif temp > 10:
            status += "Wear a coat."
        else:
            status += "It's very cold. Wear jacke"
    except:
        status = "City is not recognized"

    return status


bot.polling(none_stop=True)
