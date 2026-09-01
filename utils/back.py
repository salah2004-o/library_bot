from telebot import types

def back_button(callback_data="admin_menu"):
    return types.InlineKeyboardButton("⬅️ رجوع", callback_data=callback_data)
#photo_url = "https://cdn.spacetelescope.org/archives/images/screen/heic2007a.jpg" 