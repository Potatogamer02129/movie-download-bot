import telebot
from telebot.formatting import escape_html
from test2 import get_download_link
import requests
import os
with open ("api.txt") as f:
    API_KEY = f.read()

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello send a movie name followed by Language to start")


@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        bot.reply_to(message, "Searching, please wait...")
        link, poster_link = get_download_link(message.text)
        if link.split()[0].lower() in ("error","specify","movies"):
            bot.send_message(message.chat.id, link)
        else:
            safelink = escape_html(link)
            final_msg = f'<a href="{safelink}">Download ready — click to start</a>'
            var = requests.get(poster_link)
            with open ("temp.png", "wb") as f:
                f.write(var.content)
            if var.status_code == 200:
                bot.send_photo(message.chat.id, open("temp.png", "rb"), caption=final_msg,parse_mode="HTML")
            else:
                bot.send_message(
                message.chat.id,
                final_msg,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
            os.remove("temp.png")

    except Exception as e:
        print(e)
        bot.reply_to(message, "Failed to fetch link.")
try:
    bot.polling()
finally:
    print("Bot shut down")