# 📚 Library Bot | بوت المكتبة

> **Digital Library Management Bot for Telegram**  
> **بوت إدارة مكتبة رقمية على تيليجرام**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

<div dir="ltr">

## 🌟 Features

- 📖 **Book Catalog** - Browse digital book collection
- 🔍 **Search & Filter** - Advanced search by title, author, genre
- 📥 **Download Books** - Direct book downloads
- ⭐ **Ratings & Reviews** - Rate and review books
- 📚 **Reading List** - Create and manage personal library
- ✅ **Channel Subscription** - Verify user subscriptions
- 🏆 **Achievements** - Unlock reading achievements

---

## 🛠️ Requirements

- Python 3.8+
- SQLite Database
- Book files (PDF, EPUB, etc.)

### Dependencies
```
pyTelegramBotAPI >= 4.0
requests >= 2.28.0
```

---

## 📦 Installation

```bash
git clone https://github.com/your-username/library-bot.git
cd library-bot

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
```

---

## 🚀 Usage

```bash
python main.py
```

---

## 🎮 Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/books` | Browse books |
| `/search <title>` | Search books |
| `/download <id>` | Download book |
| `/mybooks` | Your library |
| `/rate <id> <rating>` | Rate book |
| `/admin` | Admin panel |

---

## 🗂️ Project Structure

```
library_bot/
├── main.py
├── config.py
├── book.py
├── data/
│   └── db_manager.py
├── utils/
│   ├── back.py
│   └── channels.py
├── media/
├── requirements.txt
└── README.md
```

---

## 🔐 Admin Features

- Add/Remove subscription channels
- Manage book categories
- Upload new books
- Monitor user activity

---

## 📝 License

MIT License

</div>

---

<div dir="rtl">

## 🌟 الميزات

- 📖 **فهرس الكتب** - استعرض مجموعة الكتب الرقمية
- 🔍 **البحث والتصفية** - بحث متقدم حسب العنوان والمؤلف والنوع
- 📥 **تحميل الكتب** - تحميل الكتب مباشرة
- ⭐ **التقييمات والآراء** - قيّم وقدّم آراءك حول الكتب
- 📚 **قائمة القراءة** - إنشئ وأدرّ مكتبتك الشخصية
- ✅ **التحقق من الاشتراك** - التحقق من اشتراك المستخدمين بالقنوات
- 🏆 **الإنجازات** - افتح إنجازات القراءة

---

## 🛠️ المتطلبات

- Python 3.8+
- SQLite Database
- ملفات الكتب (PDF, EPUB, إلخ)

### المكتبات المطلوبة
```
pyTelegramBotAPI >= 4.0
requests >= 2.28.0
```

---

## 📦 التثبيت

```bash
git clone https://github.com/your-username/library-bot.git
cd library-bot

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
```

---

## 🚀 الاستخدام

```bash
python main.py
```

---

## 🎮 الأوامر

| الأمر | الوصف |
|------|-------|
| `/start` | بدء البوت |
| `/books` | استعرض الكتب |
| `/search <title>` | ابحث عن كتب |
| `/download <id>` | تحميل الكتاب |
| `/mybooks` | مكتبتك |
| `/rate <id> <rating>` | قيّم الكتاب |
| `/admin` | لوحة الإدارة |

---

## 🗂️ هيكل المشروع

```
library_bot/
├── main.py
├── config.py
├── book.py
├── data/
│   └── db_manager.py
├── utils/
│   ├── back.py
│   └── channels.py
├── media/
├── requirements.txt
└── README.md
```

---

## 🔐 ميزات الإدارة

- إضافة/حذف قنوات الاشتراك
- إدارة فئات الكتب
- رفع كتب جديدة
- مراقبة نشاط المستخدمين

---

## 📝 الترخيص

MIT License

</div>

---

**Last Updated**: 2026-09-01

    # إذا مشترك في كل القنوات، اكمل ترحيبك
    user_id = message.from_user.id
    text = "مرحباً بك في مكتبة سديم للكتب.\nيتوفر الكتب لدينا عن طريق الأزرار التي ستظهر في الأسفل"
    photo_url = "https://cdn.spacetelescope.org/archives/images/screen/heic2007a.jpg"

    markup = types.InlineKeyboardMarkup(row_width=1)
    but1 = types.InlineKeyboardButton("عرض الكتب 📚", callback_data="show_books")
    but2 = types.InlineKeyboardButton("اتصل بنا 📞", callback_data="help")
    buttons = [but1, but2]

    if user_id == ADMIN_ID:
        buttons.append(types.InlineKeyboardButton("👥قسم الأدمن👥", callback_data="adminsplace"))
        buttons.append(types.InlineKeyboardButton("♟️قسم الاشتراك الإجباري♟️", callback_data="subchannels"))

    for b in buttons:
        markup.add(b)

    bot.send_message(message.chat.id, f"👋 أهلاً {message.from_user.first_name}!\n")
    bot.send_photo(message.chat.id, photo_url, caption=text, reply_markup=markup)

# التعامل مع الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "show_books":
        bot.answer_callback_query(call.id, "سيتم عرض الكتب قريباً")
        bot.send_message(call.message.chat.id, "📚 لا توجد كتب مضافة بعد.")

    elif call.data == "help":
        bot.answer_callback_query(call.id, "طلب المساعدة")
        bot.send_message(call.message.chat.id, f"{urlacc} حساب المالك للتواصل")

    elif call.data == "subchannels":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("✨إضافة قناة اشتراك إجباري✨", callback_data="add_channel"),
            types.InlineKeyboardButton("✨حذف قناة اشتراك إجباري✨", callback_data="remove_channel"),
            types.InlineKeyboardButton("✨عرض قنوات الاشتراك الإجباري✨", callback_data="list_channels"),
        )
        markup.add(back_button())
        bot.send_message(
            call.message.chat.id,
            "✨أهلاً بك في قسم الاشتراك الإجباري✨\n"
            "⌤ اضغط على زر إضافة قناة اشتراك إجباري لإضافة قناة ما إلى الاشتراك الإجباري\n"
            "⌤ اضغط على زر حذف قناة من الاشتراك الإجباري لحذف قناة ما\n"
            "⌤ اضغط على زر عرض قنوات الاشتراك الإجباري لعرض كل القنوات المضافة.",
            reply_markup=markup
        )

    elif call.data == "add_channel":
        bot.answer_callback_query(call.id, "اضغط الآن لإرسال معرف القناة لإضافتها")
        msg = bot.send_message(call.message.chat.id, "أرسل معرف القناة (@username أو ID) لإضافتها:")
        bot.register_next_step_handler(msg, add_channel)

    elif call.data == "remove_channel":
        bot.answer_callback_query(call.id, "اضغط الآن لإرسال معرف القناة لإزالتها")
        msg = bot.send_message(call.message.chat.id, "أرسل معرف القناة (@username أو ID) لإزالتها:")
        bot.register_next_step_handler(msg, remove_channel)

    elif call.data == "list_channels":
        bot.answer_callback_query(call.id, "عرض القنوات المضافة")
        if sub_channels:
            text = "\n".join(sub_channels)
        else:
            text = "لا توجد قنوات مضافة بعد."
        bot.send_message(call.message.chat.id, text)

check_bot_admin(bot, sub_channels)

bot.infinity_polling()
