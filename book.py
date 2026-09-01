from telebot import TeleBot
import requests

TOKEN = "8230938929:AAFNZCo2cwdX0GLha8pNjamvcYhzPTsvgFI"
bot = TeleBot(TOKEN)


def get_book_data(title):
    url = f"https://openlibrary.org/search.json?title={title}"
    res = requests.get(url).json()

    if res["docs"]:
        book = res["docs"][0]

        cover_id = book.get("cover_i")

        return {
            "title_en": book.get("title"),
            "author": book.get("author_name", ["Unknown"])[0],
            "year": book.get("first_publish_year"),
            "cover_url": f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else None
        }

    return None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أرسل اسم الرواية بالإنجليزي 📚")


@bot.message_handler(func=lambda message: True)
def handle_book(message):
    title = message.text

    book = get_book_data(title)

    if not book:
        bot.reply_to(message, "❌ لم يتم العثور على الرواية")
        return

    caption = f"""
📚 {book['title_en']}
✍️ {book['author']}
📅 {book['year']}
"""

    if book["cover_url"]:
        bot.send_photo(message.chat.id, book["cover_url"], caption=caption)
    else:
        bot.send_message(message.chat.id, caption)


bot.polling()