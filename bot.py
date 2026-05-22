import telebot
from telebot import types
import sqlite3

BOT_TOKEN = "8744679992:AAHdzUgtkTuwXn1ltLNUn9zY4Sd9SVqbYBM"
CHANNEL = "theom4u"

bot = telebot.TeleBot(BOT_TOKEN)

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    referrals INTEGER DEFAULT 0,
    points INTEGER DEFAULT 0
)
""")

conn.commit()


def add_user(user_id):
    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        cursor.execute(
            "INSERT INTO users (user_id, referrals, points) VALUES (?, ?, ?)",
            (user_id, 0, 0)
        )
        conn.commit()


@bot.message_handler(commands=['start'])
def start(message):

    user_id = message.from_user.id

    args = message.text.split()

    add_user(user_id)

    if len(args) > 1:

        referrer_id = int(args[1])

        if referrer_id != user_id:

            cursor.execute(
                "SELECT * FROM users WHERE user_id=?",
                (referrer_id,)
            )

            ref_user = cursor.fetchone()

            if ref_user:

                cursor.execute(
                    "UPDATE users SET referrals = referrals + 1, points = points + 10 WHERE user_id=?",
                    (referrer_id,)
                )

                conn.commit()

                bot.send_message(
                    referrer_id,
                    "🎉 New Referral Joined!\n💰 +10 Points Added"
                )

    ref_link = f"https://t.me/{bot.get_me().username}?start={user_id}"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("👥 Referral", "💰 Wallet")
    markup.add("🏆 Leaderboard")

    bot.send_message(
        message.chat.id,
        f"🔥 Welcome {message.from_user.first_name}\n\n"
        f"📢 Join Channel: @{CHANNEL}\n\n"
        f"🔗 Your Referral Link:\n{ref_link}",
        reply_markup=markup
    )


@bot.message_handler(func=lambda m: m.text == "👥 Referral")
def referral(message):

    user_id = message.from_user.id

    cursor.execute(
        "SELECT referrals FROM users WHERE user_id=?",
        (user_id,)
    )

    referrals = cursor.fetchone()[0]

    bot.send_message(
        message.chat.id,
        f"👥 Total Referrals: {referrals}"
    )


@bot.message_handler(func=lambda m: m.text == "💰 Wallet")
def wallet(message):

    user_id = message.from_user.id

    cursor.execute(
        "SELECT points FROM users WHERE user_id=?",
        (user_id,)
    )

    points = cursor.fetchone()[0]

    bot.send_message(
        message.chat.id,
        f"💰 Your Points: {points}"
    )


@bot.message_handler(func=lambda m: m.text == "🏆 Leaderboard")
def leaderboard(message):

    cursor.execute(
        "SELECT user_id, referrals FROM users ORDER BY referrals DESC LIMIT 10"
    )

    users = cursor.fetchall()

    text = "🏆 Top Referrers\n\n"

    count = 1

    for user in users:
        text += f"{count}. {user[0]} → {user[1]} referrals\n"
        count += 1

    bot.send_message(message.chat.id, text)


print("Bot Running...")

bot.infinity_polling()
