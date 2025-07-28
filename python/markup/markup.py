
import telebot
from telebot import types

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Say Hello')
    btn2 = types.KeyboardButton('Show Time')
    btn3 = types.KeyboardButton('Random Number')
    btn4 = types.KeyboardButton('About Bot')
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    bot.send_message(message.chat.id, "Welcome! Choose an option:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Say Hello')
def say_hello(message):
    bot.send_message(message.chat.id, "Hello! 👋")

@bot.message_handler(func=lambda message: message.text == 'Show Time')
def show_time(message):
    import datetime
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    bot.send_message(message.chat.id, f"Current time: {now}")

@bot.message_handler(func=lambda message: message.text == 'Random Number')
def random_number(message):
    import random
    num = random.randint(1, 100)
    bot.send_message(message.chat.id, f"Your random number is: {num}")

@bot.message_handler(func=lambda message: message.text == 'About Bot')
def about_bot(message):
    bot.send_message(message.chat.id, "This is a demo Telegram bot with markup keyboard buttons. Enjoy!")

if __name__ == "__main__":
    print("Bot is running...")
    bot.polling()
