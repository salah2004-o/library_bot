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
# نتأكد الجداول موجودة

@bot.callback_query_handler(func=lambda call: call.data.startswith("savebook_"))
def finalize_book(call):
    cat_id = int(call.data.split("_")[1])
    add_book(
        title=book_data["title"],
        author=book_data["author"],
        description=book_data["description"],
        cover_path=book_data.get("cover_path"),
        file_path=book_data["file_path"],
        category_id=cat_id,
        added_by=call.from_user.id
    )
    bot.send_message(
        call.message.chat.id,
        f"✅ تم إضافة الكتاب '{book_data['title']}' بنجاح في التصنيف رقم {cat_id}.\n\nبيانات الكتاب:\nالعنوان: {book_data['title']}\nالمؤلف: {book_data['author']}\nالوصف: {book_data['description']}"
    )
    book_data.clear()

# التعامل مع الأزرار
@bot.callback_query_handler(func=lambda call: not call.data.startswith("savebook_"))
def callback(call):
    # يجب الرد على كل callback بسرعة لتجنب خطأ Telegram API
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass

    if call.data == "show_books":
        categories = get_categories()
        if not categories:
            bot.send_message(call.message.chat.id, "🚫 لا توجد تصنيفات.")
            return

        markup = types.InlineKeyboardMarkup()
        for cat_id, name in categories:
            markup.add(types.InlineKeyboardButton(text=name, callback_data=f"cat_{cat_id}"))
        markup.add(back_button())
        bot.send_message(call.message.chat.id, "📚 اختر تصنيف:", reply_markup=markup)

    elif call.data.startswith("cat_"):
        cat_id = int(call.data.split("_")[1])
        books = get_books_by_category(cat_id)
        if not books:
            bot.send_message(call.message.chat.id, "🚫 لا توجد كتب في هذا التصنيف.")
            return

        for book_id, title, author, desc, cover, file_path in books:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📂 تحميل الكتاب", callback_data=f"book_{book_id}"))
            caption = f"📖 *{title}*\n✍️ {author}\n📝 {desc}"
            if cover and os.path.exists(cover):
                with open(cover, "rb") as photo:
                    bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=markup)
            else:
                bot.send_message(call.message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "help":
        # الرد على الاستفسار بشكل سريع
        try:
            bot.answer_callback_query(call.id, text="طلب المساعدة", show_alert=False)
        except Exception:
            pass
        bot.send_message(call.message.chat.id, f"{urlacc} حساب المالك للتواصل")

    elif call.data.startswith("book_"):
        book_id = int(call.data.split("_")[1])

        conn = get_connect()
        cur = conn.cursor()
        cur.execute("SELECT title, file_path FROM books WHERE id=%s", (book_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            title, file_path = row
            if file_path and os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    bot.send_document(call.message.chat.id, f, visible_file_name=f"{title}.pdf")
            else:
                bot.send_message(call.message.chat.id, "🚫 ملف الكتاب غير موجود حالياً.")
        else:
            bot.send_message(call.message.chat.id, "🚫 لم أجد الكتاب.")

    elif call.data == "add_category" and call.from_user.id == ADMIN_ID:
        msg = bot.send_message(call.message.chat.id, "📝 أرسل اسم التصنيف الجديد:")
        bot.register_next_step_handler(msg, save_category)

    elif call.data == "add_book" and call.from_user.id == ADMIN_ID:
        msg = bot.send_message(call.message.chat.id, "📕 أرسل عنوان الكتاب:")
        bot.register_next_step_handler(msg, save_book_step1)


# ====== حفظ التصنيف ======
def save_category(message):
    add_category(message.text)
    bot.send_message(message.chat.id, f"✅ تم إضافة التصنيف: {message.text}")


# ====== إضافة كتاب ======
book_data = {}

def save_book_step1(message):
    book_data["title"] = message.text
    msg = bot.send_message(message.chat.id, "✍️ أرسل اسم المؤلف:")
    bot.register_next_step_handler(msg, save_book_step2)

def save_book_step2(message):
    book_data["author"] = message.text
    msg = bot.send_message(message.chat.id, "📝 أرسل وصف الكتاب:")
    bot.register_next_step_handler(msg, save_book_step3)

def save_book_step3(message):
    book_data["description"] = message.text
    msg = bot.send_message(message.chat.id, "🖼️ أرسل صورة الغلاف (اختياري، اضغط /skip للتخطي):")
    bot.register_next_step_handler(msg, save_book_cover)

def save_book_cover(message):
    if message.content_type == "photo":
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)
        cover_path = f"media/covers/{file_info.file_unique_id}.jpg"
        os.makedirs("media/covers", exist_ok=True)
        with open(cover_path, "wb") as f:
            f.write(downloaded)
        book_data["cover_path"] = cover_path
    elif message.text and message.text.lower() == "/skip":
        book_data["cover_path"] = None
    else:
        bot.send_message(message.chat.id, "🚫 لازم ترسل صورة أو تكتب /skip للتخطي.")
        # نرجعه لنفس المرحلة
        msg = bot.send_message(message.chat.id, "🖼️ أرسل صورة الغلاف (اختياري، اضغط /skip للتخطي):")
        bot.register_next_step_handler(msg, save_book_cover)
        return

    msg = bot.send_message(message.chat.id, "📂 أرسل ملف الكتاب (PDF فقط):")
    bot.register_next_step_handler(msg, save_book_file)


def save_book_file(message):
    if message.content_type == "document" and message.document.mime_type == "application/pdf":
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        file_path = f"media/books/{file_info.file_unique_id}.pdf"
        os.makedirs("media/books", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(downloaded)
        book_data["file_path"] = file_path

        # بعد حفظ الكتاب، نطلب اختيار التصنيف
        categories = get_categories()
        if not categories:
            bot.send_message(message.chat.id, "🚫 ما عندك تصنيفات. لازم تضيف تصنيف أولاً.")
            return

        markup = types.InlineKeyboardMarkup()
        for cat_id, name in categories:
            markup.add(types.InlineKeyboardButton(name, callback_data=f"savebook_{cat_id}"))
        bot.send_message(message.chat.id, "📌 اختر تصنيف الكتاب:", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, "🚫 لازم ترسل ملف PDF فقط.")
        msg = bot.send_message(message.chat.id, "📂 أرسل ملف الكتاب (PDF فقط):")
        bot.register_next_step_handler(msg, save_book_file)

@bot.callback_query_handler(func=lambda call: call.data.startswith("savebook_"))
def finalize_book(call):
    cat_id = int(call.data.split("_")[1])
    add_book(
        title=book_data["title"],
        author=book_data["author"],
        description=book_data["description"],
        cover_path=book_data.get("cover_path"),
        file_path=book_data["file_path"],
        category_id=cat_id,
        added_by=call.from_user.id
    )
    # رسالة تأكيد مع بيانات التصنيف
    bot.send_message(
        call.message.chat.id,
        f"✅ تم إضافة الكتاب '{book_data['title']}' بنجاح في التصنيف رقم {cat_id}.\n\nبيانات الكتاب:\nالعنوان: {book_data['title']}\nالمؤلف: {book_data['author']}\nالوصف: {book_data['description']}"
    )
    book_data.clear()

# نسيت اربط ذا الملف في main.py
check_bot_admin(bot, sub_channels) # نتأكد البوت أدمن في القنوات