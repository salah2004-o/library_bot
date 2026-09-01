import telebot
from telebot import types
from config import ADMIN_ID, urlacc, bot, sub_channels
from utils.back import back_button
from utils.channels import check_bot_admin
from data.db_manager import (
    get_categories,
    get_books_by_category,
    add_book,
    add_category,
    create_tables,
    get_connect
)
import os
import n
# نتأكد الجداول موجودة
create_tables()


# تسجيل المستخدمين في قاعدة البيانات
def register_user(user):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (telegram_id, first_name)
        VALUES (%s, %s)
        ON CONFLICT (telegram_id) DO NOTHING
    """, (user.id, user.first_name))
    conn.commit()
    cur.close()
    conn.close()


# رسالة ترحيب
@bot.message_handler(commands=["start"])
def welcome(message):
    register_user(message.from_user)  # تسجيل المستخدم أول ما يدخل

    # تحقق الاشتراك الإجباري
    not_subscribed = []
    for channel in sub_channels:
        try:
            member = bot.get_chat_member(channel, message.from_user.id)
            if member.status not in ["member", "administrator", "creator"]:
                not_subscribed.append(channel)
        except:
            bot.send_message(
                message.chat.id,
                f"⚠️ ما قدرت أتحقق من القناة {channel}. تأكد إن البوت أدمن فيها."
            )
            return

    if not_subscribed:
        bot.send_message(
            message.chat.id,
            "🚫 لازم تشترك أولاً في القنوات التالية:\n" + "\n".join(not_subscribed)
        )
        return

    # لوحة البداية
    user_id = message.from_user.id
    text = "مرحباً بك في مكتبة سديم للكتب.\n📚 اختر من القائمة بالأسفل"
    photo_url = "https://cdn.spacetelescope.org/archives/images/screen/heic2007a.jpg"

    markup = types.InlineKeyboardMarkup(row_width=1)
    but1 = types.InlineKeyboardButton("عرض الكتب 📚", callback_data="show_books")
    but2 = types.InlineKeyboardButton("اتصل بنا 📞", callback_data="help")
    buttons = [but1, but2]

    if user_id == ADMIN_ID:
        buttons.append(types.InlineKeyboardButton("➕إضافة كتاب", callback_data="add_book"))
        buttons.append(types.InlineKeyboardButton("➕إضافة تصنيف", callback_data="add_category"))
        buttons.append(types.InlineKeyboardButton("👥قسم الأدمن👥", callback_data="adminsplace"))
        buttons.append(types.InlineKeyboardButton("♟️قسم الاشتراك الإجباري♟️", callback_data="subchannels"))

    for b in buttons:
        markup.add(b)

    bot.send_message(message.chat.id, f"👋 أهلاً {message.from_user.first_name}!\n")
    bot.send_photo(message.chat.id, photo_url, caption=text, reply_markup=markup)




check_bot_admin(bot, sub_channels)
bot.infinity_polling()
