import telebot

TOKEN = "8744679992:AAHdzUgtkTuwXn1ltLNUn9zY4Sd9SVqbYBM"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔥 Bot Working Hai")

print("Bot Running...")

bot.infinity_polling()
